export type HomeInfo = {
  _id: string;
  name: string;
  code: string;
};

export type AuthUser = {
  _id: string;
  name: string;
  email: string;
  home?: HomeInfo;
};

export type AuthResponse = {
  token: string;
  user: AuthUser;
};
