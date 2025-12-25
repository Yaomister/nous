import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useState,
} from "react";
import { api } from "../axios";
import { useTokenStore } from "../token";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState();

  const loadUser = useCallback(async () => {
    console.error("LOADING USER");
    const token = useTokenStore.getState().token;
    console.error(token);
    if (!token) {
      setUser(null);
      return;
    }

    try {
      const { data: _user } = await api.get("/user/me");
      setUser(_user);
      console.error("SET USER");
    } catch (err) {
      console.error(err);
      setUser(null);
    }
  }, []);

  useEffect(() => {
    loadUser();
  }, [loadUser]);

  const login = useCallback(async () => {
    console.error("FUCKING LOGIN CALLED");
    loadUser();
  }, [loadUser]);

  return (
    <AuthContext.Provider value={{ user, login }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
