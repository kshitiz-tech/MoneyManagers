import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";

export default function Login() {
  return (
    <div className="min-h-full bg-white p-6 flex items-center">
      <div className="w-full max-w-md mx-auto">
        <div className="mb-8 text-center">
          <h1 className="text-4xl mb-2">M M</h1>
          <p className="text-gray-600">Money Managers</p>
        </div>

        <form className="space-y-4">
          <div>
            <Label htmlFor="username">Username</Label>
            <Input
              id="username"
              type="text"
              placeholder="Enter your username"
              className="h-12 mt-1"
            />
          </div>

          <div>
            <Label htmlFor="password">Password</Label>
            <Input
              id="password"
              type="password"
              placeholder="Enter your password"
              className="h-12 mt-1"
            />
          </div>

          <button type="button" className="w-full h-12 mt-6 bg-blue-600 text-white rounded-md">
            Login
          </button>

          <div className="text-center mt-4">
            <span className="text-sm text-blue-600">Forgot Password?</span>
          </div>

          <div className="text-center text-sm text-gray-600 mt-4">
            Don't have an account?{" "}
            <span className="text-blue-600">Register</span>
          </div>
        </form>
      </div>
    </div>
  );
}
