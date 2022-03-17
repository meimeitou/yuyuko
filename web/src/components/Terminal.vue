<template>
  <q-badge :color="connectColor"> 连接状态: {{ status }} </q-badge>
  <div
    style="width: 100%; height: calc(100% - 50px)"
    id="terminal"
    class="terminal"
  />
</template>

<script lang="ts">
import { ref, defineComponent } from "vue";
import { io } from "socket.io-client";
import "xterm/css/xterm.css";
import "xterm/lib/xterm.js";
import { Terminal } from "xterm";
import { FitAddon } from "xterm-addon-fit";
import { SearchAddon } from "xterm-addon-search";
import { WebLinksAddon } from "xterm-addon-web-links";

export default defineComponent({
  Name: "Terminal",
  props: {
    host: {
      type: String,
      required: true,
    },
    port: {
      type: Number,
      default: 22,
      required: true,
    },
    user: {
      type: String,
      required: true,
    },
    password: {
      type: String,
      required: true,
    },
    socketURI: {
      type: String,
      default:
        window.location.protocol +
        "//" +
        window.location.hostname +
        ":" +
        window.location.port +
        "/pty",
    },
    socketPath: {
      type: String,
      default: "/socket/terminal.io",
    },
  },
  setup() {
    var rows = 45;
    var cols = 50;
    const term = new Terminal({
      rendererType: "canvas", // 渲染类型
      rows: rows, // 行数
      cols: cols, // 不指定行数，自动回车后光标从下一行开始
      convertEol: true, // 启用时，光标将设置为下一行的开头
      scrollback: 150, // 终端中的回滚量
      disableStdin: false, // 是否应禁用输入。
      // cursorStyle: "underline", // 光标样式
      cursorBlink: true, // 光标闪烁
      theme: {
        foreground: "#7e9192", // 字体
        background: "#002833", // 背景色
        cursor: "help", // 设置光标
      },
      macOptionIsMeta: true,
    });
    var fit = new FitAddon();
    term.loadAddon(fit);
    term.loadAddon(new SearchAddon());
    term.loadAddon(new WebLinksAddon());
    // init socket
    const options = {
      path: "/socket/terminal.io",
    }; //Options object to pass into SocketIO
    //     http[s]://<domain>:<port>[/<namespace>]
    const uri =
      window.location.protocol +
      "//" +
      window.location.hostname +
      ":" +
      window.location.port +
      "/pty";
    //     http[s]://<domain>:<port>[/<namespace>]
    // const socket = io("http://10.18.30.212:5588/pty", options); //options object is Optional
    const socket = io(uri, options);
    return {
      fit,
      socket,
      status: ref("disconnected"),
      term, // 保存terminal实例
      rows,
      cols,
      connectColor: ref("green"),
    };
  },
  created() {
    window.addEventListener("resize", this.debounce);
  },
  unmounted() {
    window.removeEventListener("resize", this.debounce);
  },
  beforeUnmount() {
    this.socket.close();
    this.term.dispose();
  },
  mounted() {
    this.socket.on("connect_failed", () => {
      this.term.writeln("sd");
    });
    this.socket.on("error", () => {
      this.term.writeln("sd");
    });
    this.initTerminal();
    // 连接后端
    this.socket.on("connect", () => {
      this.socket.emit("ssh", {
        host: this.host,
        port: this.port,
        user: this.user,
        password: this.password,
        rows: this.term.rows,
        cols: this.term.cols,
      });
      this.status = "connected";
      this.connectColor = "green";
    });
    // 绑定socket方法
    // 后端输出到终端
    this.socket.on("pty-output", (data) => {
      // console.log("new output received from server:", data.output);
      this.term.write(data.output);
    });
    // 断开连接
    this.socket.on("disconnect", () => {
      this.socket.close();
      this.connectColor = "red";
      this.status = "disconnected";
    });
    // this.fitToscreen();
    // console.log(this.term.rows, this.term.cols);
  },
  methods: {
    initTerminal() {
      const modalRoot = document.getElementById("terminal") as HTMLElement;
      this.term.open(modalRoot);
      // this.fit.fit();
      this.term.resize(this.cols, this.rows);
      this.fit.fit();
      this.term.focus();
      this.term.writeln("\x1b[1;31m" + "Welcome to Yuyuko Web Terminal! ");
      this.term.writeln(
        "\x1b[37m" + "Powered by: TonyTin, https://github.com/roygbip/yuyuko"
      );
      this.term.writeln("");
      // 监听终端输入
      this.term.onData((data) => {
        console.log("key pressed in browser:", data);
        // this.term.write(data);
        this.socket.emit("ptyinput", { input: data });
      });
      // ctrl + d
      // this.term.attachCustomKeyEventHandler((e) => {
      //   if (e.ctrlKey && e.key === "d") {
      //     this.socket.emit("disconnect_request");
      //     return false;
      //   }
      //   return true;
      // });
    },
    // 终端大小调整
    fitToscreen() {
      this.fit.fit();
      const dims = { cols: this.term.cols, rows: this.term.rows };
      console.log("sending new dimensions to server's pty", dims);
      this.socket.emit("resize", dims);
    },
    debounce() {
      let timeout;
      clearTimeout(timeout);
      timeout = setTimeout(() => {
        this.fitToscreen();
      }, 100);
    },
  },
});
</script>
