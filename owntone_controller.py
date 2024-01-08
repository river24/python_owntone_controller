import asyncio
import signal
import logging
import os
import yaml
from typing import Dict

from evdev import list_devices, InputDevice, ecodes
import httpx


QUEUE_TIMEOUT = 5.0

DEFAULT_CONFIG = {
    "api_scheme": "http",
    "api_host": "127.0.0.1:3689",
    "device_name": "SayoDevice FiiO KB1 Keyboard",
    "event_mapping": {
        165: "prev", 164: "play",
        163: "next",
        114: "volDown",
        115: "volUp",
        113: "mute",
    }
}


def generate_control_path(player_event, state, volume):
    if player_event == "play":
        if state == "play":
            path = "/api/player/pause"
        else:
            path = "/api/player/play"
    elif player_event == "prev":
        path = "/api/player/previous"
    elif player_event == "next":
        path = "/api/player/next"
    elif player_event == "volDown":
        path = "/api/player/volume?step=-1"
    elif player_event == "volUp":
        path = "/api/player/volume?step=+1"
    elif player_event == "mute":
        path = f"/api/player/volume?volume={volume}"
    else:
        return None
    return path


async def get_status(config: Dict):
    try:
        async with httpx.AsyncClient() as client:
            r = await client.get(f"{config['api_scheme']}://{config['api_host']}/api/player")
    except Exception as e:
        logging.error(e)
        return None, None
    if r.status_code != httpx.codes.ok:
        return None, None
    status = r.json()
    return status.get("state", None), status.get("volume", None)


async def event_handler(queue: asyncio.Queue, config: Dict):
    state = None
    volume = None
    unmute = None

    while state is None and volume is None:
        (
            _state,
            _volume,
        ) = await get_status(config)
        if _state and _volume:
            state = _state
            volume = _volume
        else:
            await asyncio.sleep(5)

    while True:
        try:
            get_await = queue.get()
            event = await asyncio.wait_for(get_await, QUEUE_TIMEOUT)
            if event.code not in config["event_mapping"].keys():
                continue
            player_event = config["event_mapping"][event.code]
            if player_event == "mute":
                if volume == 0 and unmute:
                    volume = unmute
                    unmute = None
                else:
                    unmute = volume
                    volume = 0
            elif player_event in ["volDown", "volUp"]:
                if unmute:
                    player_event = "mute"  # override
                    volume = unmute
                    if player_event == "volDown" and volume > 0:
                        volume -= 1
                    elif player_event == "volUp" and volume < 100:
                        volume += 1
                    unmute = None
            path = generate_control_path(player_event, state, volume)
            if not path:
                continue
            async with httpx.AsyncClient() as client:
                _ = await client.put(f"{config['api_scheme']}://{config['api_host']}{path}")
            (
                _state,
                _volume,
            ) = await get_status(config)
            if _state and _volume:
                state = _state
                volume = _volume
            queue.task_done()
        except asyncio.TimeoutError:
            (
                _state,
                _volume,
            ) = await get_status(config)
            if _state and _volume:
                state = _state
                volume = _volume


async def device_watcher(queue: asyncio.Queue, config: Dict):
    while True:
        target_device_path = None
        all_devices = [InputDevice(path) for path in list_devices()]
        for device in all_devices:
            if device.name == config["device_name"]:
                target_device_path = device.path
        if not target_device_path:
            await asyncio.sleep(1)
            continue
        try:
            target_input_device = InputDevice(target_device_path)
            async for event in target_input_device.async_read_loop():
                if event.type != ecodes.EV_KEY:
                    continue
                if event.type != 1:
                    continue
                if event.value != 1:
                    continue
                await queue.put(event)
        except Exception as e:
            logging.error(e)
            await asyncio.sleep(1)


async def shutdown(signal, loop):
    logging.info(f"Received exit signal {signal.name}...")
    tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]

    [task.cancel() for task in tasks]

    logging.info("Cancelling outstanding tasks")
    await asyncio.gather(*tasks, return_exceptions=True)
    loop.stop()


def load_config():
    config = DEFAULT_CONFIG.copy()
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    config_file = os.path.join(ROOT_DIR, "configs", "config.yml")
    try:
        with open(config_file) as f:
            loaded_config = yaml.load(f, Loader=yaml.Loader)
            for key in DEFAULT_CONFIG.keys():
                if key in loaded_config:
                    config[key] = loaded_config[key]
    except Exception as e:
        logging.error(f"Failed to load config from {config_file}: {e}")
        logging.error(f"Use 'DEFAULT_CONFIG'")
        config = DEFAULT_CONFIG.copy()
    return config


def main():
    loop = asyncio.get_event_loop()

    config = load_config()
    logging.info(f"Config: {config}")

    signals = (signal.SIGHUP, signal.SIGTERM, signal.SIGINT)
    for s in signals:
        loop.add_signal_handler(s, lambda s=s: asyncio.create_task(shutdown(s, loop)))

    queue = asyncio.Queue()

    try:
        loop.create_task(event_handler(queue, config))
        loop.create_task(device_watcher(queue, config))
        loop.run_forever()
    finally:
        logging.info("Successfully shutdown service")
        loop.close()


if __name__ == "__main__":
    main()
