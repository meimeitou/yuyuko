<template>
  <q-btn @click="toggle()" label="快速连接" color="accent" class="q-ml-sm" />
  <q-dialog v-model="dialog" :position="posit" persistent>
    <q-card style="width: 1200px; max-width: 90vw">
      <q-bar>
        <q-icon name="terminal" />
        <div>9:34</div>
        <q-space />
        <q-btn dense flat icon="close" v-close-popup>
          <q-tooltip>Close</q-tooltip>
        </q-btn>
      </q-bar>
      <q-card-section class="q-pt-none">
        <!-- form -->
        <div class="q-pa-md" style="padding: 5px">
          <div class="row items-center">
            <div class="col-1">
              <div class="text-subtitle1">快速历史:</div>
            </div>
            <div class="col" style="padding-right: 5px">
              <q-select
                color="purple-12"
                dense
                filled
                clearable
                v-model="chooseHistory"
                :options="localSSHHistory"
                label="history"
              >
                <template v-slot:option="{ itemProps, opt }">
                  <q-item v-bind="itemProps">
                    <q-item-section>
                      <q-item-label v-html="opt.label" />
                    </q-item-section>
                    <q-item-section side>
                      <q-btn
                        size="12px"
                        @click.stop="deleteHistory(opt)"
                        flat
                        round
                        color="primary"
                        icon="close"
                      />
                    </q-item-section>
                  </q-item>
                </template>
              </q-select>
            </div>
          </div>
          <q-separator style="margin-top: 5px"></q-separator>
          <div class="row" style="margin-top: 5px">
            <div class="col-6">
              <div class="row" style="margin-top: 5px">
                <div class="text-subtitle1">主机列表:</div>
              </div>
              <div class="col" style="height: 100%">
                <q-form
                  @submit="newHost"
                  class="q-gutter-md"
                  style="height: 100%"
                >
                  <q-markup-table dense flat style="height: 100%">
                    <thead>
                      <tr>
                        <th class="text-left"></th>
                        <th class="text-left"><b>Host</b></th>
                        <th class="text-left"><b>Port</b></th>
                        <th class="text-left"><b>Comments</b></th>
                      </tr>
                    </thead>
                    <tbody>
                      <template v-for="item in listHost" :key="item.host">
                        <tr
                          @click="chooseHost(item)"
                          :class="item === choosedHost ? 'rowBg' : ''"
                          style="cursor: pointer"
                        >
                          <td class="text-left">
                            <q-btn
                              size="9px"
                              @click.stop="delHost(item)"
                              flat
                              round
                              color="red"
                              icon="close"
                              ><q-tooltip>删除主机</q-tooltip></q-btn
                            >
                          </td>
                          <td class="text-left">{{ item.host }}</td>
                          <td class="text-left">{{ item.port }}</td>
                          <td class="text-left">{{ item.comments }}</td>
                        </tr>
                      </template>
                      <!-- add 主机 -->
                      <tr style="margin-bottom: 15px">
                        <td class="text-left">
                          <q-btn
                            round
                            flat
                            size="9px"
                            color="positive"
                            icon="add"
                            type="submit"
                            ><q-tooltip>添加主机</q-tooltip></q-btn
                          >
                        </td>
                        <td class="text-left" style="padding: 0px">
                          <q-input
                            dense
                            v-model="inputHost.host"
                            style="margin-top: 4px; padding-bottom: 10px"
                            lazy-rules
                            label="host"
                            :rules="[(val) => (val && val.length > 0) || '']"
                          />
                        </td>
                        <td class="text-left" style="padding: 0px">
                          <q-input
                            dense
                            v-model="inputHost.port"
                            style="margin-top: 4px; padding-bottom: 10px"
                            label="port"
                            lazy-rules
                            type="number"
                            :rules="[(val) => val > 0 || '错误']"
                          />
                        </td>
                        <td class="text-left" style="padding: 0px">
                          <q-input
                            dense
                            label="comments"
                            v-model="inputHost.comments"
                            style="margin-top: 4px; padding-bottom: 10px"
                          />
                        </td>
                      </tr>
                    </tbody>
                  </q-markup-table>
                </q-form>
              </div>
            </div>
            <q-separator vertical inset style="margin: 0px 4px" />
            <div class="col">
              <div class="row">
                <div class="text-subtitle1">用户选择:</div>
              </div>
              <div class="row" style="margin-top: 10px">
                <!-- 添加用户 -->
                <q-btn
                  round
                  size="10px"
                  color="primary"
                  icon="add"
                  class="q-ml-sm"
                >
                  <q-tooltip>添加用户</q-tooltip>
                  <q-menu
                    transition-show="jump-right"
                    transition-hide="jump-left"
                    anchor="top right"
                    self="center left"
                    v-model="showAddUser"
                  >
                    <div
                      class="row items-center no-wrap q-pa-md"
                      style="padding: 5px"
                    >
                      <div class="column">
                        <div class="text-h6 q-mb-md">Add</div>
                        <q-form @submit="newUser" class="q-gutter-md">
                          <q-input
                            dense
                            filled
                            v-model="inputUser.label"
                            label="Lable"
                            style="margin-top: 4px; padding-bottom: 10px"
                            lazy-rules
                            :rules="[
                              (val) => (val && val.length > 0) || '必填',
                            ]"
                          />
                          <q-input
                            filled
                            dense
                            v-model="inputUser.user"
                            label="User"
                            style="margin-top: 4px; padding-bottom: 10px"
                            lazy-rules
                            :rules="[
                              (val) => (val && val.length > 0) || '必填',
                            ]"
                          />
                          <q-input
                            filled
                            dense
                            type="password"
                            v-model="inputUser.password"
                            label="Passowrd"
                            style="margin-top: 4px; padding-bottom: 10px"
                            lazy-rules
                            :rules="[
                              (val) => (val && val.length > 0) || '必填',
                            ]"
                          />
                          <div class="text-center" style="margin-top: 4px">
                            <q-btn
                              dense
                              class="full-width"
                              label="Save"
                              type="submit"
                              color="primary"
                            />
                          </div>
                        </q-form>
                      </div>
                    </div>
                  </q-menu>
                </q-btn>
              </div>
              <div class="row">
                <div class="q-gutter-sm">
                  <template v-for="item in localUser" :key="item.label">
                    <q-radio
                      v-model="selectUser"
                      checked-icon="task_alt"
                      unchecked-icon="panorama_fish_eye"
                      :val="item"
                      :label="item.label"
                    />
                  </template>
                </div>
              </div>
              <!-- decode show -->
              <div class="row" style="margin-top: 10px">
                <div class="q-px-sm">
                  当前选中用户:
                  <strong class="rowBg" v-if="selectUserDecode !== null">{{
                    selectUserDecode === null
                      ? ""
                      : `${selectUserDecode.user}/(******)`
                  }}</strong>
                  <q-btn
                    v-if="selectUser !== null"
                    size="9px"
                    @click="deleteUser"
                    flat
                    round
                    color="red"
                    icon="close"
                  >
                    <q-tooltip>删除用户</q-tooltip></q-btn
                  >
                </div>
              </div>
            </div>
          </div>
        </div>
      </q-card-section>
      <q-card-actions align="right" style="padding: 0px 10px 5px 0px">
        <q-space></q-space>
        使用连接命令：
        <strong>ssh&nbsp;&nbsp;</strong>
        <strong
          >{{
            selectUserDecode === null ? `(null)` : selectUserDecode.user
          }}@</strong
        >
        <strong
          >{{
            choosedHost.host === "" ? `(null)` : choosedHost.host
          }}&nbsp;</strong
        >
        <strong>
          -oPort={{
            choosedHost.port === "" ? `(null)` : choosedHost.port
          }}</strong
        >
        <q-space></q-space>
        <div>
          <q-btn flat label="连接终端" color="primary" @click="enterConnect" />
        </div>
      </q-card-actions>
    </q-card>
  </q-dialog>
</template>

<script lang="ts">
import { ref, defineComponent } from "vue";
import {
  SSHLocalHistory,
  SSHLocalHistoryOption,
  SSHUser,
  SSHHost,
} from "@/lib/types";
import api from "@/lib/api/tool";
import { mapState } from "vuex";
import tools from "@/lib/tools";

export default defineComponent({
  Name: "SSHHistory",
  props: {
    position: {
      type: String,
      required: false,
      default: "top",
    },
  },
  emits: ["setConnect"],
  setup(props) {
    return {
      dialog: ref(false),
      posit: props.position,
      chooseHistory: ref<SSHLocalHistoryOption | null>(null),
      // listUser: ref<Array<SSHUser>>([]),
      listHost: ref<Array<SSHHost>>([]), // decod
      selectUser: ref<SSHUser | null>(null),
      selectUserDecode: ref<SSHUser | null>(null),
      showAddUser: ref(false),
      inputUser: ref<SSHUser>({
        label: "",
        user: "",
        password: "",
      }),
      inputHost: ref<SSHHost>({
        host: "",
        port: "22",
        comments: "",
      }),
      choosedHost: ref<SSHHost>({
        host: "",
        port: "22",
        comments: "",
      }),
    };
  },
  computed: {
    ...mapState({
      /* eslint-disable */
      localSSHHistory: (state: any) =>
        state.localSSHHistory as Array<SSHLocalHistoryOption>,
      localUser: (state: any) => state.localUser as Array<SSHUser>,
      localHost: (state: any) => state.localHost as Array<SSHHost>
    })
  },
  mounted() {
    if (this.localHost.length > 0) {
      api.aes(false, "", ["comments"], this.localHost).then((res) => {
        const items = res.data.data as SSHHost[];
        this.listHost = items;
      });
    }
  },
  watch: {
    chooseHistory(newValue: SSHLocalHistoryOption | null) {
      if (newValue !== null) {
        // decode
        api
          .aes(
            false,
            "",
            [],
            [
              {
                host: newValue.value.host,
                port: newValue.value.port,
                user: newValue.value.user,
                password: newValue.value.password
              }
            ]
          )
          .then((res) => {
            const item = res.data.data[0] as SSHLocalHistory;
            this.$emit("setConnect", item);
            this.dialog = false;
            this.chooseHistory = null;
          });
      }
    },
    selectUser(newValue: SSHUser | null) {
      if (newValue !== null) {
        api.aes(false, "", ["label"], [newValue]).then((res) => {
          var item = res.data.data[0] as SSHUser;
          this.selectUserDecode = item;
        });
      }
    }
  },
  methods: {
    deleteHistory(item: SSHLocalHistoryOption) {
      console.log(item);
      this.$store.commit("delLocalSSHHistory", item);
    },
    newUser() {
      api.aes(true, "", ["label"], [this.inputUser]).then((res) => {
        var item = res.data.data[0] as SSHUser;
        // item.label = this.inputUser.label;
        this.$store.commit("addLocalUser", item);
        // clear
        this.inputUser.label = "";
        this.inputUser.user = "";
        this.inputUser.password = "";
        this.showAddUser = false;
      });
    },
    deleteUser() {
      this.$store.commit("delLocalUser", this.selectUser);
      this.selectUser = null;
      this.selectUserDecode = null;
    },
    newHost() {
      api.aes(true, "", ["comments"], [this.inputHost]).then((res) => {
        var item = res.data.data[0] as SSHHost;
        this.$store.commit("addLocalHost", item);

        const host = { ...this.inputHost } as SSHHost;
        this.listHost.push(host);
        // clear input
        this.inputHost.host = "";
        this.inputHost.port = "22";
        this.inputHost.comments = "";
      });
    },
    delHost(item: SSHHost) {
      api.aes(true, "", ["comments"], [item]).then((res) => {
        var encode = res.data.data[0] as SSHUser;
        // 删除存储
        this.$store.commit("delLocalHost", encode);
        // 删除列表
        const index = this.listHost.findIndex(
          (obj) => obj.host === item.host && obj.port === item.port
        );
        if (index > -1) {
          this.listHost.splice(index, 1);
        }
      });
    },
    chooseHost(item: SSHHost) {
      this.choosedHost = item;
    },
    getBg(item: SSHHost) {
      item === this.choosedHost ? "rowBg" : "";
    },
    toggle() {
      this.dialog = true;
    },
    enterConnect() {
      if (
        this.selectUserDecode === null ||
        this.choosedHost.host === "" ||
        this.choosedHost.port === ""
      ) {
        tools.errMsg("连接参数缺失，请检查主机和用户选择");
        return;
      }
      const con = {
        name: "",
        host: this.choosedHost.host,
        port: this.choosedHost.port,
        user: this.selectUserDecode.user,
        password: this.selectUserDecode.password
      } as SSHLocalHistory;
      this.$emit("setConnect", con);
      this.dialog = false;
    }
  }
});
</script>

<style lang="scss">
@import "../styles/quasar.variables.scss";
@import "../styles/quasar.scss";
.rowBg {
  background-color: $purple-2;
}
</style>
