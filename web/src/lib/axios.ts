import axios from "axios";
import router from "@/router";
import tools from "@/lib/tools";
import { AxiosResponse } from "axios";
axios.interceptors.response.use(onSuccess, onError);
axios.defaults.timeout = 1000 * 30;

/* eslint-disable */
function onError(e: any) {
  if (e.response) {
    // 请求已发出，服务器返回的 http 状态码不是 2xx，例如：400，500，对应上面的 1
    // console.log(e.response)s
    switch (e.response.status) {
      case 400:
        e.message = "错误请求";
        // tool.errMsg(e.response.data.msg);
        break;
      case 401:
        router.push("/login");
        break;
      case 404:
        e.message = "请求路径不存在";
        // tool.errMsg("请求路径不存在");
        break;
      case 422:
        e.message = "请求参数错误";
        tools.errMsg(e.response.data.message);
        break;
      case 500:
        e.message = "服务器请求错误";
        tools.errMsg("服务器请求错误");
        break;
      default:
      // tool.errMsg(e.response.data.msg);
    }
  } else if (e.request) {
    // 请求已发出，但没有收到响应，例如：断网，对应上面的 4
    console.log(e.request);
    tools.errMsg("后端服务无响应");
  } else {
    // 请求被取消或者发送请求时异常，对应上面的 2 & 3
    console.log("error", e.message);
    tools.errMsg("请求异常");
  }
  return Promise.reject(e);
}

function onSuccess(res: AxiosResponse) {
  return res;
}

export default axios;
