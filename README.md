# scroll

![logo.gif](screens/art.png?raw=true "art.png")

A bot to play ASCII art for the Internet Relay Chat (IRC) protocol.

###### Information
The bot will join the `channel` defined in config.py and the `#scroll` channel.

ASCII that exceeds `max_lines` can only be played in the `#scroll` channel.

Turning the bot off will part the bot from the channel defined in the config, but all commands will still function in the `#scroll` channel.

###### Note
The `ascii_list.py` file will generate a text file containing a numbered list of every file in the `/data/ascii` directory. You can upload that list to pastebin or a web-server, and then put the link in `/data/ascii/list.txt` so you can have a `.ascii list` command that just sends a link instead of overflowing the channel with file names.

###### Commands
| Command | Description |
| --- | --- |
| .ascii random | Play a random ASCII file. |
| .ascii search \<query> | Search through the ASCII files for \<query>. |
| .ascii stop | Stop playing the current ASCII being scrolled / Stop the auto scroll loop. |
| .ascii \<name> | Play the \<name> ASCII file. |

###### Admin Commands
| Command | Description |
| --- | --- |
| .ascii auto | Automatically scroll random ASCII files. |

###### Admin Commands (Private Message)
| Command | Description |
| --- | --- |
| .config | View the config settings. |
| .config \<setting> \<value> | Change \<setting> to \<value>. |
| .ignore | View the ignore list. |
| .ignore add \<nick> \<host> | Add a user to the ignore list. |
| .ignore del \<nick> \<host> | Remove a user from the ignore list. |
| .off | Toggle the usage of the bot commands. |
| .on | Toggle the usage of the bot commands. |

###### Config
| Setting | Description |
| --- | --- |
| cmd_throttle | Delay between command usage for flood control. |
| msg_throttle | Delay between each line send to the channel. |
| max_lines | Maximum number of lines an ASCII can be to be played outside of the *#scroll* channel. |
| max_results | Maximum number of results returned from a search. |