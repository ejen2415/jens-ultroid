from . import *
import datetime


@vc_asst("play")
async def play_music_(event):

    # TODO - file, cplay, radio

    xx = await eor(event, "`Processing...`")

    args = event.text.split(" ", 1)
    chat = event.chat_id
    from_user = event.sender_id

    try:
        song = args[1]
    except IndexError:
        return await eod(xx, "Please specify a song name !", time=10)

    await eor(xx, "`Downloading and converting...`")
    TS = datetime.datetime.now().strftime("%H:%M:%S")
    song, thumb, song_name, duration = await download(event, song, chat, TS)

    if not ultSongs.group_call.is_connected:
        # check if vc_Client is in call
        done = await vc_joiner(event, event.chat_id)
        if not done:
            return
        await xx.reply(
            "**Now playing:** `{}`\n**Duration:** `{}`\n**Chat:** `{}`\n**Requested by:** `{}`".format(
                song_name, time_formatter(duration * 1000), chat, from_user
            ),
            file=thumb,
        )

        ultSongs.group_call.input_filename = song
        await xx.delete()
    else:
        add_to_queue(chat, song, song_name, thumb, from_user, duration)
        return await eor(
            xx,
            f"Added **{song_name}** to queue at #{list(VC_QUEUE[chat].keys())[-1]}",
        )
