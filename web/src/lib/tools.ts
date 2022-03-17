import { Dialog } from "quasar";

export default {
  errMsg(msg: string): void {
    Dialog.create({
      title: "错误",
      message: msg,
    });
  },
  okMsg(msg: string): void {
    Dialog.create({
      title: "提示",
      message: msg,
    });
  },
};
