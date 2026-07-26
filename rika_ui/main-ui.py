from textual.app import App, ComposeResult
from textual.containers import Horizontal, VerticalScroll, Vertical
from textual.widgets import Button, Input, Label, Static


class ConsolUI(App):
    CSS_PATH = "layouts.tcss"

    def compose(self) -> ComposeResult:

        # Titel
        yield Static(
            "[bold green]Mini KI[/bold green]",
            id="main_title",
        )

        # Hauptbereich
        with Horizontal(id="main_content"):

            # Linke Sidebar
            with VerticalScroll(id="chat_sidebar", classes="box"):

                yield Label("Chats", classes="box_title")

                yield Button(
                    "+ Neuer Chat",
                    id="newchat",
                )

                yield Button(
                    "Chat 1",
                    id="chat1",
                )

                yield Button(
                    "Chat 2",
                    id="chat2",
                )

            # Rechte Chatbox
            with Vertical(id="chat_area", classes="box"):

                yield Label(
                    "ChatBox",
                    classes="box_title",
                )

                yield Static(
                    "Chatverlauf.",
                    id="chat_history",
                )

                with Horizontal(id="input_row"):

                    yield Input(
                        placeholder="Nachricht eingeben ...",
                        id="message_input",
                    )

                    yield Button(
                        "Senden",
                        id="send_button",
                        variant="primary",
                    )

        # Shortcut-Leiste unten
        yield Static(
            "[bold blue]New Chat = Ctrl + N[/bold blue] | "
            "[bold blue]Settings = Ctrl + S[/bold blue] | "
            "[bold red]Delete Chat = Ctrl + X[/bold red] | "
            "[bold blue]Exit = Ctrl + Q[/bold blue] | "
            "[bold blue]Hide = Ctrl + H[/bold blue]",
            classes="bottom_bar",
        )

    # Button-Events
    def on_button_pressed(self, event: Button.Pressed) -> None:

        if event.button.id == "newchat":
            self.create_new_chat()

        elif event.button.id == "send_button":
            print("Nachricht senden")

    def create_new_chat(self) -> None:
        print("Neuen Chat erstellen")


if __name__ == "__main__":
    ConsolUI().run()