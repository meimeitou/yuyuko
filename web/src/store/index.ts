import { createStore } from "vuex";
import createPersistedState from "vuex-persistedstate";
import { SSHLocalHistoryOption, SSHHost, SSHUser } from "@/lib/types";
export default createStore({
  state: {
    localSSHHistory: [] as SSHLocalHistoryOption[],
    localHost: [] as SSHHost[],
    localUser: [] as SSHUser[],
  },
  mutations: {
    addLocalSSHHistory(state, item: SSHLocalHistoryOption) {
      const index = state.localSSHHistory.findIndex(
        (obj) => obj.label === item.label
      );
      if (index > -1) {
        // find
        state.localSSHHistory.splice(index, 1);
      }
      // push new
      state.localSSHHistory.push(item);
    },
    delLocalSSHHistory(state, item: SSHLocalHistoryOption) {
      const index = state.localSSHHistory.findIndex(
        (obj) => obj.label === item.label
      );
      if (index > -1) {
        state.localSSHHistory.splice(index, 1);
      }
    },
    addLocalUser(state, item: SSHUser) {
      const index = state.localUser.findIndex(
        (obj) => obj.label === item.label
      );
      if (index > -1) {
        // find
        state.localUser.splice(index, 1);
      }
      // push new
      state.localUser.push(item);
    },
    delLocalUser(state, item: SSHUser) {
      const index = state.localUser.findIndex(
        (obj) => obj.label === item.label
      );
      if (index > -1) {
        state.localUser.splice(index, 1);
      }
    },
    addLocalHost(state, item: SSHHost) {
      const index = state.localHost.findIndex(
        (obj) => obj.host === item.host && obj.port === item.port
      );
      if (index > -1) {
        // find
        state.localHost.splice(index, 1);
      }
      // push new
      state.localHost.push(item);
    },
    delLocalHost(state, item: SSHHost) {
      const index = state.localHost.findIndex(
        (obj) => obj.host === item.host && obj.port === item.port
      );
      if (index > -1) {
        state.localHost.splice(index, 1);
      }
    },
  },
  plugins: [createPersistedState()],
  actions: {},
  modules: {},
});
