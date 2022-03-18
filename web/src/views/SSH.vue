<template>
  <q-dialog v-model="prompt" persistent>
    <q-card style="min-width: 350px">
      <q-card-section>
        <div class="text-h6">Name</div>
      </q-card-section>
      <q-card-section class="q-pt-none">
        <q-input
          dense
          v-model="inputName"
          autofocus
          lazy-rules
          :rules="[(val) => (val && val.length > 0) || 'Please input name']"
        />
      </q-card-section>

      <q-card-actions align="right" class="text-primary">
        <q-btn flat label="取消" v-close-popup />
        <q-btn flat label="保存" @click="saveConnect()" />
      </q-card-actions>
    </q-card>
  </q-dialog>
  <div class="q-pa-md">
    <q-form
      @submit="onSubmit"
      @reset="onReset"
      ref="myForm"
      class="q-gutter-md"
    >
      <div class="row">
        <div class="col-2" style="padding-right: 5px">
          <q-input
            filled
            clearable
            dense
            v-model="connect.host"
            label="Host *"
            lazy-rules
            :rules="[(val) => (val && val.length > 0) || 'Please type host']"
          />
        </div>
        <div class="col-1" style="padding-right: 5px">
          <q-input
            filled
            clearable
            dense
            type="number"
            v-model="connect.port"
            label="Port *"
            lazy-rules
            :rules="[
              (val) => (val !== null && val !== '') || 'Please input port',
              (val) => val > 0 || 'Please type a real port',
            ]"
          />
        </div>
        <div class="col-2" style="padding-right: 5px">
          <q-input
            filled
            dense
            clearable
            v-model="connect.user"
            label="User *"
            lazy-rules
            :rules="[(val) => (val && val.length > 0) || 'Please input user']"
          />
        </div>
        <div class="col-2" style="padding-right: 5px">
          <q-input
            filled
            dense
            clearable
            type="password"
            v-model="connect.password"
            label="Password *"
            lazy-rules
            :rules="[
              (val) => (val && val.length > 0) || 'Please input password',
            ]"
          />
        </div>
        <div class="col" style="padding-right: 5px">
          <div>
            <q-btn label="连接终端" type="submit" color="positive" />
            <q-btn label="清空连接" type="reset" color="info" class="q-ml-sm" />
            <q-btn
              @click="prompt = true"
              label="保存连接"
              color="primary"
              class="q-ml-sm"
            >
              <q-tooltip>保存到快速连接中的快速历史中</q-tooltip></q-btn
            >
            <SSHHistory ref="historyComp" @setConnect="setConnect"></SSHHistory>
          </div>
        </div>
      </div>
    </q-form>
    <div class="row item-center" v-if="connectTabs.length < 1">
      <div class="col-12 text-center">
        <q-badge rounded outline color="dark" class="text-subtitle1">
          当前未连接终端，点击连接终端或者使用快速连接
        </q-badge>
        <q-separator style="height: 0px"></q-separator>
        <img
          alt="logo"
          src="../assets/magic.gif"
          style="height: 300px; margin-top: 10px"
        />
      </div>
    </div>
    <div class="row">
      <div class="col-12">
        <q-card flat>
          <q-tabs
            no-caps
            v-model="tab"
            dense
            inline-label
            class="bg-grey-3"
            active-color="primary"
            indicator-color="primary"
            align="justify"
            :breakpoint="0"
          >
            <template v-for="item in connectTabs" :key="item.name">
              <q-tab :name="item.name" :icon="item.icon" :label="item.label">
                <q-btn
                  size="8px"
                  @click.stop="closeTab(item)"
                  flat
                  color="primary"
                  icon="close"
                />
              </q-tab>
            </template>
          </q-tabs>
          <q-tab-panels
            :keep-alive="true"
            v-model="tab"
            style="padding: 0px 0px"
          >
            <template v-for="item in connectTabs" :key="item">
              <q-tab-panel :name="item.name" style="padding: 0px 0px">
                <Terminal
                  :terminalID="item.id"
                  :host="item.host"
                  :port="item.port"
                  :user="item.user"
                  :password="item.password"
                ></Terminal>
              </q-tab-panel>
            </template>
          </q-tab-panels>
        </q-card>
      </div>
    </div>
  </div>
</template>

<script lang="ts">
import { ComponentPublicInstance, ref, defineComponent } from "vue";
import Terminal from "@/components/Terminal.vue";
import { SSHTab, SSHLocalHistory, SSHLocalHistoryOption } from "@/lib/types";
import api from "@/lib/api/tool";
import SSHHistory from "@/components/SSHHistory.vue";
// import local from "@/lib/local";
import { mapState } from "vuex";

export default defineComponent({
  name: "SSH",
  setup() {
    /* eslint-disable */
    const myForm = ref<ComponentPublicInstance<any>>();
    const historyComp = ref<InstanceType<typeof SSHHistory>>();
    return {
      myForm,
      historyComp,
      tab: ref(""),
      prompt: ref(false),
      inputName: ref(""),
      connect: ref({
        host: ref("localhost"),
        port: ref(22),
        user: ref(""),
        password: ref("")
      }),
      connectTabs: ref<Array<SSHTab>>([])
    };
  },
  components: {
    Terminal,
    SSHHistory
  },
  computed: {
    ...mapState({
      /* eslint-disable */
      localSSHHistory: (state: any) =>
        state.localSSHHistory as Array<SSHLocalHistoryOption>
    })
  },
  methods: {
    onSubmit() {
      const id = this.makeid(10);
      this.tab = id;
      this.connectTabs.push({
        name: id,
        label: `${this.connect.host}:${this.connect.port}`,
        icon: "terminal",
        host: this.connect.host,
        port: this.connect.port,
        user: this.connect.user,
        password: this.connect.password
      });
    },
    onReset() {
      this.connect = {
        host: "localhost",
        port: 22,
        user: "",
        password: ""
      };
    },
    // 保存当前连接
    saveConnect(): void {
      this.myForm?.validate().then((success: boolean) => {
        if (success) {
          if (this.inputName === "") {
            return;
          }
          // encode
          api
            .aes(
              true,
              "",
              [],
              [
                {
                  host: this.connect.host,
                  port: `${this.connect.port}`,
                  user: this.connect.user,
                  password: this.connect.password
                }
              ]
            )
            .then((res) => {
              console.log(res.data.data);
              const item = res.data.data[0] as SSHLocalHistory;
              item.name = this.inputName;
              // save
              this.$store.commit("addLocalSSHHistory", {
                label: item.name,
                value: item
              } as SSHLocalHistoryOption);
            });
          this.prompt = false;
        } else {
          return;
        }
      });
    },
    setConnect(event: SSHLocalHistory) {
      this.connect.host = event.host;
      this.connect.port = Number.parseInt(event.port);
      this.connect.user = event.user;
      this.connect.password = event.password;
      this.onSubmit();
    },
    makeid(length: number) {
      var result = "";
      var characters =
        "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789";
      var charactersLength = characters.length;
      for (var i = 0; i < length; i++) {
        result += characters.charAt(
          Math.floor(Math.random() * charactersLength)
        );
      }
      return result;
    },
    closeTab(item: SSHTab) {
      const index = this.connectTabs.indexOf(item);

      if (index > -1) {
        this.connectTabs.splice(index, 1);
      }
      if (this.tab !== item.name) {
        return;
      }
      if (this.connectTabs.length > 0 && item.name === this.tab) {
        this.tab = this.connectTabs[this.connectTabs.length - 1].name;
      } else {
        this.tab = "";
      }
    }
  }
});
</script>
