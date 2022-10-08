# Hackathon

"configurations": [
    {
        "name": "Python: Main",
        "type": "python",
        "args": ["2017", "False"],
        "request": "launch",
        "program": "${workspaceFolder}/main.py",
        "console": "integratedTerminal"
    },
    {
        "name": "Python: UI",
        "type": "python",
        "args": ["2017", "True"],
        "request": "launch",
        "program": "${workspaceFolder}/gui/dash_gui.py",
        "console": "integratedTerminal"
    }
]