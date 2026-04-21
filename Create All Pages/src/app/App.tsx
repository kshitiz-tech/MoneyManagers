import { RouterProvider } from 'react-router';
import { router } from './routes';
import { IPhoneFrame } from './components/IPhoneFrame';

export default function App() {
  return (
    <IPhoneFrame>
      <RouterProvider router={router} />
    </IPhoneFrame>
  );
}