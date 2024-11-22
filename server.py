import websockets
import asyncio
import re

# notes = ['C4', 'D4', 'E4', 'G4', 'A4', 'C5', 'D5', 'E5', 'G5', 'A5']
task = ""
target_pattern = []
collected_beats = {}
collected_beats_str = ""

task_pattern = r"Task \d+"
target_p_pattern = r"\d+"

file_path = "log.csv"


# Modify the function to accept only the websocket argument
async def handle_client(websocket):
    global task
    global target_pattern
    global collected_beats
    global collected_beats_str

    async for message in websocket:
        print(f"Received: {message}")

        # Task x
        if re.fullmatch(task_pattern, message):
            task = message

            f = open(file_path, "w")
            f.close()

        # targetPattern
        elif re.fullmatch(target_p_pattern, message):
            target_pattern = list(message)

        # END
        elif message == "END":
            for ele in collected_beats_str.split(" "):
                if ele == " " or ele == "":
                    break

                key, beat = ele.split(":")
                collected_beats[int(beat)] = key

            f = open(file_path, "a")

            f.write(f"{task},0\n")

            for i in range(len(target_pattern)):
                if i in collected_beats:
                    f.write(f"{collected_beats[i]},{target_pattern[i]}\n")
                else:
                    f.write(f"0,{target_pattern[i]}\n")

            f.close()

            target_pattern = []
            collected_beats = {}
            collected_beats_str = ""

        # Beat
        else:
            collected_beats_str += message + " "


# Start the WebSocket server
async def main():
    # Only pass the handle_client function without the extra argument
    async with websockets.serve(handle_client, "localhost", 6789):  # Port 6789
        print("WebSocket server is running on ws://localhost:6789")
        await asyncio.Future()  # Run forever


if __name__ == "__main__":
    asyncio.run(main())
