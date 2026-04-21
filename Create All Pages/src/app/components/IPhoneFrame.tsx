import { ReactNode } from "react";

interface IPhoneFrameProps {
  children: ReactNode;
}

export function IPhoneFrame({ children }: IPhoneFrameProps) {
  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-900 p-4">
      {/* iPhone 17 Pro Max Frame */}
      <div className="relative bg-black rounded-[60px] p-3 shadow-2xl">
        {/* iPhone bezel */}
        <div className="relative bg-black rounded-[50px] overflow-hidden" style={{ width: '430px', height: '932px' }}>
          {/* Dynamic Island */}
          <div className="absolute top-0 left-1/2 transform -translate-x-1/2 w-[126px] h-[37px] bg-black rounded-b-[20px] z-50"></div>
          
          {/* Screen content */}
          <div className="relative w-full h-full bg-white overflow-y-auto overflow-x-hidden">
            {children}
          </div>
        </div>
      </div>
    </div>
  );
}
