#!/usr/bin/env python

import asyncio
import websockets
import json
import os

# This function will run for each connected client
async def shell_handler(websocket, path):
    # Start the shell as a subprocess
    process = await asyncio.create_subprocess_shell(
        "python -u -m app.main",
        stdout=asyncio.subprocess.PIPE,
        stdin=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE
    )

    # --- Helper functions to forward data --- #

    async def forward_stream_to_client(stream, stream_name):
        """Reads from a stream (stdout/stderr) and sends it to the client."""
        while True:
            line = await stream.readline()
            if not line:
                break
            # Send data as a JSON object to distinguish between output and file tree updates
            await websocket.send(json.dumps({"type": "output", "stream": stream_name, "data": line.decode('utf-8')}))

    async def get_file_tree(path='.'):
        """Generates a dictionary representing the file tree."""
        tree = {'name': os.path.basename(path), 'type': 'directory', 'children': []}
        try:
            for name in os.listdir(path):
                item_path = os.path.join(path, name)
                if os.path.isdir(item_path):
                    tree['children'].append(await get_file_tree(item_path))
                else:
                    tree['children'].append({'name': name, 'type': 'file'})
        except OSError:
            pass # Ignore permission errors
        return tree

    # --- Main Logic --- #

    # Start tasks to forward stdout and stderr to the client
    stdout_task = asyncio.create_task(forward_stream_to_client(process.stdout, 'stdout'))
    stderr_task = asyncio.create_task(forward_stream_to_client(process.stderr, 'stderr'))

    try:
        # Listen for messages from the client
        async for message in websocket:
            # The client sends commands to the shell's stdin
            process.stdin.write(message.encode('utf-8') + b'\n')
            await process.stdin.drain()

            # After each command, send an updated file tree
            await asyncio.sleep(0.1) # Give the command a moment to execute
            tree = await get_file_tree()
            await websocket.send(json.dumps({"type": "file_tree", "data": tree}))

    finally:
        # Clean up when the client disconnects
        stdout_task.cancel()
        stderr_task.cancel()
        process.terminate()
        await process.wait()

# Start the WebSocket server
start_server = websockets.serve(shell_handler, "0.0.0.0", 8765)

print("WebSocket server started on port 8765")
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
