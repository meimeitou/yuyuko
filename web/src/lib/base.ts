import axios from "@/lib/axios";
import { AxiosPromise } from "axios";
import api from "@/lib/base";
export default {
  /* eslint-disable */
  post(path: string, data: any, type: string): AxiosPromise {
    return axios({
      method: "post",
      url: path,
      data: data,
      headers: { "Content-Type": type }
    });
  },
  /* eslint-disable */
  postJson(path: string, data: any): AxiosPromise {
    return api.post(path, data, "application/json");
  },
  /* eslint-disable */
  postForm(path: string, data: any): AxiosPromise {
    return api.post(path, data, "multipart/form-data");
  },
  /* eslint-disable */
  get(path: string, params: any): AxiosPromise {
    return axios.get(path, {
      params: params
    });
  }
};
