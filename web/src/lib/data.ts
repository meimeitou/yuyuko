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

export { menuList };
