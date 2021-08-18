# -*- coding: utf-8 -*-

from time import sleep

from g_python.hmessage import HMessage
from g_python.hpacket import HPacket

from gex.commands.cmd import CMD
from gex.commands.notyping import NoTypingCmd
from gex.setup import date, ext, log


class Interaction(CMD):
    (loop_awake, loop_autosit, loop_autosign, blocked) = (True, True, True, False)
    timeout = 30

    def init(self) -> None:
        """[summary]"""
        log.info("Initializing awake command!")
        ext.intercept_out(self.speech_out, "Chat", "async_modify")
        no_typing = NoTypingCmd(ext)
        no_typing.init()

    def speech_out(self, message: HMessage) -> None:
        """[summary]

        Args:
            message (HMessage): [description]
        """
        packet = message.packet
        text = packet.read_string().lower()

        if text == "!help":
            message.is_blocked = True
            ext.send_to_client(
                '{in:Whisper}{i:2}{s:"Available commands:"}{i:0}{i:33}{i:0}{i:-1}'
            )
            ext.send_to_client(
                '{in:Whisper}{i:2}{s:"!aw on and !aw off"}{i:0}{i:33}{i:0}{i:-1}'
            )
            ext.send_to_client(
                '{in:Whisper}{i:2}{s:"!nt on and !nt off"}{i:0}{i:33}{i:0}{i:-1}'
            )
            ext.send_to_client(
                '{in:Whisper}{i:2}{s:"!ats on and !ats off"}{i:0}{i:33}{i:0}{i:-1}'
            )
            ext.send_to_client(
                '{in:Whisper}{i:2}{s:"!atsg on and !atsg off"}{i:0}{i:33}{i:0}{i:-1}'
            )

        if text == "!aw help":
            log.info("Viewing awake helper")
            message.is_blocked = True
            ext.send_to_client(
                '{in:Whisper}{i:2}{s:"Use the awake command to always stay awake in habbos rooms :D"}{i:0}{i:33}{i:0}{i:-1}'
            )

        if text == "!aw on":
            log.info("Awake enabled!")
            message.is_blocked = True
            self.loop_awake = True
            ext.send_to_client(
                '{in:Whisper}{i:2}{s:"Awake enabled!"}{i:0}{i:33}{i:0}{i:-1}'
            )
            self.awake()

        if text == "!aw off":
            log.info("Awake disabled!")
            message.is_blocked = True
            self.loop_awake = False
            ext.send_to_client(
                '{in:Whisper}{i:2}{s:"Awake disabled!"}{i:0}{i:33}{i:0}{i:-1}'
            )

        if text == "!nt off":
            log.info("No Typing disabled!")
            message.is_blocked = True
            self.blocked = False
            ext.send_to_client(
                '{in:Whisper}{i:2}{s:"No Typing disabled!"}{i:0}{i:33}{i:0}{i:-1}'
            )

        if text == "!ats on":
            log.info("Auto Sit enabled!")
            message.is_blocked = True
            self.loop_autosit = True
            ext.send_to_client(
                '{in:Whisper}{i:2}{s:"Auto Sit enabled!"}{i:0}{i:33}{i:0}{i:-1}'
            )
            self.auto_sit()

        if text == "!ats off":
            log.info("Auto Sit disabled!")
            message.is_blocked = True
            self.loop_autosit = False
            ext.send_to_client(
                '{in:Whisper}{i:2}{s:"Auto Sit disabled!"}{i:0}{i:33}{i:0}{i:-1}'
            )

        if text == "!atsg on":
            log.info("Auto Sign enabled!")
            message.is_blocked = True
            self.loop_autosign = True
            ext.send_to_client(
                '{in:Whisper}{i:2}{s:"Auto Sign enabled!"}{i:0}{i:33}{i:0}{i:-1}'
            )
            self.auto_sign()

        if text == "!atsg off":
            log.info("Auto Sign disabled!")
            message.is_blocked = True
            self.loop_autosign = False
            ext.send_to_client(
                '{in:Whisper}{i:2}{s:"Auto Sign disabled!"}{i:0}{i:33}{i:0}{i:-1}'
            )

    def awake(self) -> None:
        """[summary]"""
        while self.loop_awake:
            log.info("Calling awake cmd")
            content = f"Datetime: {date.get_date_now()}"
            ext.send_to_server(HPacket("Whisper", content, 1, 1))
            sleep(self.timeout)

    def typing(self, message: HMessage) -> None:
        """[summary]

        Args:
            message (HMessage): [description]
        """
        log.info("Typing handler")
        message.is_blocked = self.blocked

    def auto_sit(self) -> None:
        """[summary]"""
        while self.loop_autosit:
            log.info("Calling Auto Sit")
            ext.send_to_server("{out:ChangePosture}{i:1}")
            sleep(0.2)

    def auto_sign(self) -> None:
        """[summary]"""
        while self.loop_autosign:
            log.info("Calling Auto Sign")
            ext.send_to_server("{out:Sign}{i:1}")
            sleep(4)
