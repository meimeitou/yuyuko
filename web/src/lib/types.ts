interface Item {
  icon: string;
  label: string;
  separator: boolean;
}

interface SSHTab {
  name: string;
  icon: string;
  label: string;
  host: string;
  port: number;
  user: string;
  password: string;
}

interface SSHLocalHistory {
  name: string;
  host: string;
  port: string;
  user: string;
  password: string;
}

interface SSHLocalHistoryOption {
  label: string;
  value: SSHLocalHistory;
}

interface SSHUser {
  label: string;
  user: string;
  password: string;
}

interface SSHHost {
  host: string;
  port: string;
  comments: string;
}

export {
  Item,
  SSHTab,
  SSHLocalHistory,
  SSHLocalHistoryOption,
  SSHUser,
  SSHHost,
};
