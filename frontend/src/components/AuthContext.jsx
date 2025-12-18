import { createContext, useContext, useState } from "react";

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [bearerToken, setBearerToken] = useState("");
  return (
    <AuthContext.Provider value={{ bearerToken, setBearerToken }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
