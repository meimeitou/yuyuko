<template>
  {{ status }}
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
  setup() {
    var rows = 100;
    var cols = 40;
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
    const options = { path: "/socket/terminal.io" }; //Options object to pass into SocketIO
    //     http[s]://<domain>:<port>[/<namespace>]
    const socket = io("http://10.18.30.212:5588/pty", options); //options object is Optional

    return {
      fit,
      socket,
      status: ref("disconnected"),
      term, // 保存terminal实例
      rows,
      cols,
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
    // 连接后端
    this.socket.on("connect", () => {
      this.initTerminal();
      this.fitToscreen();
      this.status = "connected";
    });
    // 绑定socket方法
    // 后端输出到终端
    this.socket.on("pty-output", (data) => {
      console.log("new output received from server:", data.output);
      this.term.write(data.output);
    });
    // 断开连接
    this.socket.on("disconnect", () => {
      this.status = "disconnect";
    });
  },
  methods: {
    initTerminal() {
      const modalRoot = document.getElementById("terminal") as HTMLElement;
      this.term.open(modalRoot);
      // this.fit.fit();
      this.term.resize(this.rows, this.cols);
      this.fit.fit();
      this.term.focus();
      this.term.writeln("Welcome to Yuyuko Terminal!");
      // 监听终端输入
      this.term.onData((data) => {
        // console.log("key pressed in browser:", data);
        // this.term.write(data);
        this.socket.emit("ptyinput", { input: data });
      });
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
