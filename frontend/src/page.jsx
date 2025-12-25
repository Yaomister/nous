import { Outlet } from "react-router-dom";
import "./stylesheets/page.css";
import { NavBar } from "./components/NavBar";

export const Page = () => {
  return (
    <div className="page">
      <NavBar />
      <Outlet />
    </div>
  );
};
