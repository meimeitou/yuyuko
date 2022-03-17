import base from "@/lib/base";
import { AxiosPromise } from "axios";
export default {
  /* eslint-disable */
  aes(encrypt: boolean, salt: string, skips: Array<String>, data: any[]): AxiosPromise {
    return base.postJson("/api/aes", {
      encrypt: encrypt,
      salt: salt,
      skips: skips,
      data: data
    });
  }
};
