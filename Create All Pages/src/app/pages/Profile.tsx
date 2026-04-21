import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { ArrowLeft, User as UserIcon } from "lucide-react";

export default function Profile() {
  const name = "John Doe";

  return (
    <div className="min-h-full bg-gray-50 pb-20">
      <div className="w-full p-4">
        <div className="flex items-center gap-3 mb-6 pt-4">
          <button className="h-10 w-10 inline-flex items-center justify-center rounded-md">
            <ArrowLeft className="w-6 h-6" />
          </button>
          <h1 className="text-2xl">Profile</h1>
        </div>

        {/* Profile Info */}
        <div className="bg-white border border-gray-200 p-4 mb-4">
          <div className="flex flex-col items-center">
            <div className="w-20 h-20 bg-gray-200 rounded-full flex items-center justify-center mb-4">
              <UserIcon className="w-10 h-10 text-gray-500" />
            </div>
            <div className="text-center">
              <p className="text-xl mb-2">{name}</p>
              <span className="text-blue-600 text-sm">Edit Name</span>
            </div>
          </div>
        </div>

        {/* Change Password */}
        <div className="bg-white border border-gray-200 p-4 mb-4">
          <h2 className="text-lg mb-3">Change Password</h2>
          <button className="w-full h-12 bg-blue-600 text-white rounded-md">
            Change Password
          </button>
        </div>

        {/* Delete Account */}
        <div className="bg-white border border-gray-200 p-4 mb-4">
          <h2 className="text-lg text-red-600 mb-3">Danger Zone</h2>
          <button className="w-full h-12 bg-red-600 text-white rounded-md">
            Delete Account
          </button>
        </div>

        {/* Logout */}
        <div className="bg-white border border-gray-200 p-4">
          <button className="w-full h-12 border border-gray-300 rounded-md">
            Logout
          </button>
        </div>
      </div>
    </div>
  );
}
