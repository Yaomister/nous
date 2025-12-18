import { Outlet } from "react-router-dom";
import "./stylesheets/page.css";

export const Page = () => {
  return (
    <div className="page">
      <Outlet />
    </div>
  );
};
