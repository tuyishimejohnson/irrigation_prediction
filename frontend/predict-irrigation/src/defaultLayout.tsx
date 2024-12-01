import { Outlet, NavLink } from "react-router-dom";

const activeLinks = ({ isActive }: { isActive: boolean }) =>
  isActive ? "text-blue-500" : undefined;

const DefaultLayout = () => {
  return (
    <div>
      <nav className="flex justify-between py-6 px-32 font-noto items-center fixed left-0 right-0 z-20 bg-white">
        <div>
          <NavLink to={"/"}>Smart Irrigation</NavLink>
        </div>

        <div className="flex justify-between gap-5 items-center">
          <div className="flex gap-10">
            <NavLink to={"/about"} className={activeLinks}>
              About
            </NavLink>
            <NavLink to={"/predict"} className={activeLinks}>
              Predict
            </NavLink>
            <NavLink to={"/Results"} className={activeLinks}>
              Contacts
            </NavLink>
            <NavLink to={"/Results"} className={activeLinks}>
              Contacts
            </NavLink>
          </div>
        </div>
      </nav>

      <div className="pt-20">
        <Outlet />
      </div>
    </div>
  );
};

export default DefaultLayout;
