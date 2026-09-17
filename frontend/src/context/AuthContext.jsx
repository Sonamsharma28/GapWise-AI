import React, { createContext, useContext, useState, useEffect } from 'react';
import { getMe, login as apiLogin, register as apiRegister } from '../api/auth';

const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(localStorage.getItem('gapwise_token'));
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const checkAuth = async () => {
      if (token) {
        try {
          const res = await getMe();
          setUser(res.data);
        } catch (error) {
          console.error("Token invalid or expired", error);
          setToken(null);
          setUser(null);
          localStorage.removeItem('gapwise_token');
        }
      }
      setLoading(false);
    };
    checkAuth();
  }, [token]);

  const login = async (email, password) => {
    const res = await apiLogin({ email, password });
    const { token: jwtToken, user: userData } = res.data;
    localStorage.setItem('gapwise_token', jwtToken);
    setToken(jwtToken);
    setUser(userData);
    return userData;
  };

  const register = async (name, email, password, role, classCode = null) => {
    const payload = { name, email, password, role };
    if (classCode && classCode.trim()) {
      payload.class_code = classCode.trim();
    }
    const res = await apiRegister(payload);
    const { token: jwtToken, user: userData } = res.data;
    localStorage.setItem('gapwise_token', jwtToken);
    setToken(jwtToken);
    setUser(userData);
    return userData;
  };


  const logout = () => {
    localStorage.removeItem('gapwise_token');
    setToken(null);
    setUser(null);
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        login,
        register,
        logout,
        isAuthenticated: !!user
      }}
    >
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
