import { ReactNode } from "react";

interface ButtonProps {
  children: ReactNode;
}

interface ButtonProps {
  children: ReactNode;
  className?: string;
  type?: string;
  onSubmit?: (event:React.FormEvent<HTMLFormElement>) => void;
}

const Button = ({ children, className }: ButtonProps) => {
  return (
    <div>
      <button className={`${className}`}>{children}</button>
    </div>
  );
};

export default Button;
