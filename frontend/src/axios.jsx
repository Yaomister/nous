import axios from "axios";
import { useTokenStore } from "./token";

const api = axios.create({
  baseURL: "http://localhost:8000",
  withCredentials: true,
});

api.interceptors.request.use((config) => {
  const token = useTokenStore.getState().token;
  if (token) {
    console.error("SETTING THE BEARER TOKEN");
    config.headers.Authorization = `Bearer ${token}`;
  }

  return config;
});

api.interceptors.response.use(
  (res) => res,
  async (err) => {
    if (err.config?.url?.includes("/refresh")) return Promise.reject(err);

    if (err.response?.status != 401) return Promise.reject(err);

    try {
      const res = await api.post("/user/refresh", null);

      const token = res.data.token;

      useTokenStore.getState().setToken(token);

      err.config.headers.Authorization = `Bearer ${token}`;
      return api.request(err.config);
    } catch (err) {
      useTokenStore.getState().clearToken();
      return Promise.reject(err);
    }
  }
);

export { api };
