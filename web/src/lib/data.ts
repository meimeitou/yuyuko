import { SSHShortCut } from "@/lib/types";
const menuList = [
  {
    icon: "inbox",
    label: "Home",
    separator: true,
    to: "/",
  },
  {
    icon: "terminal",
    label: "SSH",
    separator: false,
    to: "/ssh",
  },
  {
    icon: "terminal",
    label: "Curl",
    separator: false,
    to: "/curl",
  },
  {
    icon: "terminal",
    label: "Spider",
    separator: false,
    to: "/spider",
  },
  {
    icon: "terminal",
    label: "Tools",
    separator: true,
    to: "/tools",
  },
  {
    icon: "help",
    iconColor: "primary",
    label: "About",
    separator: false,
    to: "/about",
  },
];

const shortCutList = [
  {
    command: "sudo su",
    description: "to root",
    sudo: true,
  },
  {
    command: "",
    description: "paste user password",
    sudo: true,
  },
  {
    command: "kubectl get node",
    description: "show k8s node",
    sudo: false,
  },
  {
    command: "tmux new -s tmp",
    description: "tmux terminal",
    sudo: false,
  },
] as Array<SSHShortCut>;

export { menuList, shortCutList };
