from datetime import datetime

from textual.app import App, ComposeResult
from textual.containers import Horizontal, Vertical, VerticalScroll
from textual.widgets import Button, Input, Label, RichLog, Static


class ConsolUI(App):
    CSS_PATH = "css/layouts.tcss"

    def compose(self) -> ComposeResult:
        # Titel
        yield Static(
            "[bold green]RIKA[/bold green]",
            id="main_title",
        )

        # Hauptbereich
        with Horizontal(id="main_content"):

            # Linke Spalte
            with Vertical(id="left_column"):

                # Chat-Liste
                with VerticalScroll(
                    id="chat_sidebar",
                    classes="box",
                ):
                    yield Label(
                        "Chats",
                        classes="box_title",
                    )

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

                # RIKA-Konsole
                with Vertical(
                    id="console_box",
                    classes="box",
                ):
                    yield Label(
                        "RIKA-Konsole",
                        classes="box_title",
                    )

                    yield RichLog(
                        id="console_output",
                        wrap=True,
                        highlight=True,
                        markup=True,
                        auto_scroll=True,
                    )

            # Rechter Chatbereich
            with Vertical(
                id="chat_area",
                classes="box",
            ):
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

        # Untere Shortcut-Leiste
        yield Static(
            "[bold blue]New Chat = Ctrl + N[/bold blue] | "
            "[bold blue]Settings = Ctrl + S[/bold blue] | "
            "[bold red]Delete Chat = Ctrl + X[/bold red] | "
            "[bold blue]Exit = Ctrl + Q[/bold blue]",
            classes="bottom_bar",
        )

    def on_mount(self) -> None:
        """Wird ausgeführt, wenn die Oberfläche vollständig geladen wurde."""
        self.log_message(
            "RIKA-Konsole wurde gestartet.",
            log_type="system",
        )

    def on_button_pressed(self, event: Button.Pressed) -> None:
        """Verarbeitet Klicks auf Buttons."""

        if event.button.id == "newchat":
            self.create_new_chat()

        elif event.button.id == "send_button":
            self.send_message()

        elif event.button.id in {"chat1", "chat2"}:
            self.open_chat(event.button.label.plain)

    def create_new_chat(self) -> None:
        """Erstellt später einen neuen Chat."""
        self.log_message(
            "Neuer Chat wurde erstellt.",
            log_type="success",
        )

    def open_chat(self, chat_name: str) -> None:
        """Öffnet einen ausgewählten Chat."""
        self.log_message(
            f"{chat_name} wurde geöffnet.",
            log_type="info",
        )

    def send_message(self) -> None:
        """Liest das Eingabefeld aus und verarbeitet die Nachricht."""
        message_input = self.query_one("#message_input", Input)
        message = message_input.value.strip()

        if not message:
            self.log_message(
                "Es wurde keine Nachricht eingegeben.",
                log_type="warning",
            )
            return

        chat_history = self.query_one("#chat_history", Static)

        chat_history.update(
            f"[bold cyan]Du:[/bold cyan] {message}"
        )

        self.log_message(
            "Nachricht wurde an RIKA übergeben.",
            log_type="info",
        )

        self.log_message(
            "RIKA verarbeitet die Nachricht ...",
            log_type="system",
        )

        message_input.value = ""
        message_input.focus()

    def log_message(
        self,
        message: str,
        log_type: str = "info",
    ) -> None:
        """Schreibt eine Meldung in die sichtbare RIKA-Konsole."""

        console = self.query_one("#console_output", RichLog)
        timestamp = datetime.now().strftime("%H:%M:%S")

        colors = {
            "info": "blue",
            "success": "green",
            "warning": "yellow",
            "error": "red",
            "system": "magenta",
        }

        color = colors.get(log_type, "white")

        console.write(
            f"[dim]{timestamp}[/dim] "
            f"[{color}]{message}[/{color}]"
        )


if __name__ == "__main__":
    ConsolUI().run()