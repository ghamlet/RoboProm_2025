import main


"""
1 - красный (брак)
2 - оранж - wait
3 - хрупкая - зелён
4 - синий - не хрупкая
5 - син&зел - нету объекта
0 - orange OFF - all off
"""


class Lamp:
    def __init__(self, ip: str, port: int, state: int = 2):
        self.state = state
        self.ip = ip
        self.port = port

    def set_state(self, state: int = 0):
        self.state = state
        main.server.send_message(
            str.encode(
                f"id:1:state:{self.state}", "utf-8",
            ),
            self.ip,
            self.port,
        )

    def waiting_commands(self):
        self.set_state(2)

    def command_received(self):
        self.set_state(0)

    def defect(self):
        self.set_state(1)

    def delicate(self):
        self.set_state(3)

    def not_delicate(self):
        self.set_state(4)

    def not_object(self):
        self.set_state(5)
