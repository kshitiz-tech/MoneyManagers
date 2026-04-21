import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { BarChart3, CreditCard, User, Plus } from "lucide-react";

interface Transaction {
  id: string;
  type: "Income" | "Expense";
  amount: number;
  note: string;
  date: string;
}

export default function Dashboard() {
  const selectedMonth = "March";
  const selectedYear = "2024";

  // Mock data
  const transactions: Transaction[] = [
    { id: "1", type: "Income", amount: 5000, note: "Salary", date: "2024-03-01" },
    { id: "2", type: "Expense", amount: 1200, note: "Rent", date: "2024-03-02" },
    { id: "3", type: "Expense", amount: 300, note: "Groceries", date: "2024-03-05" },
    { id: "4", type: "Income", amount: 500, note: "Freelance", date: "2024-03-10" },
    { id: "5", type: "Expense", amount: 150, note: "Utilities", date: "2024-03-15" },
  ];

  const totalIncome = transactions
    .filter((t) => t.type === "Income")
    .reduce((sum, t) => sum + t.amount, 0);

  const totalExpense = transactions
    .filter((t) => t.type === "Expense")
    .reduce((sum, t) => sum + t.amount, 0);

  const total = totalIncome - totalExpense;

  return (
    <div className="relative min-h-full bg-gray-50 pb-20">
      <div className="w-full p-4">
        <h1 className="text-2xl text-center mb-6 pt-4">Dashboard</h1>

        {/* Date Selector */}
        <div className="bg-white p-4 mb-4 border border-gray-200">
          <div className="flex gap-3">
            <Select value={selectedMonth}>
              <SelectTrigger className="flex-1 h-12">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {["January", "February", "March", "April", "May", "June", "July", "August", "September", "October", "November", "December"].map((month) => (
                  <SelectItem key={month} value={month}>
                    {month}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
            <Select value={selectedYear}>
              <SelectTrigger className="flex-1 h-12">
                <SelectValue />
              </SelectTrigger>
              <SelectContent>
                {["2022", "2023", "2024", "2025", "2026"].map((year) => (
                  <SelectItem key={year} value={year}>
                    {year}
                  </SelectItem>
                ))}
              </SelectContent>
            </Select>
          </div>
        </div>

        {/* Summary Cards */}
        <div className="grid grid-cols-3 gap-3 mb-4">
          <div className="bg-white p-3 border border-gray-200">
            <p className="text-xs text-gray-600 mb-1">Income</p>
            <p className="text-lg text-green-600">${totalIncome}</p>
          </div>
          <div className="bg-white p-3 border border-gray-200">
            <p className="text-xs text-gray-600 mb-1">Expense</p>
            <p className="text-lg text-red-600">${totalExpense}</p>
          </div>
          <div className="bg-white p-3 border border-gray-200">
            <p className="text-xs text-gray-600 mb-1">Total</p>
            <p className={`text-lg ${total >= 0 ? "text-blue-600" : "text-red-600"}`}>
              ${total}
            </p>
          </div>
        </div>

        {/* Transactions */}
        <div className="bg-white border border-gray-200 p-4">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-lg">Transactions</h2>
            <button className="h-9 px-4 bg-blue-600 text-white rounded-md text-sm inline-flex items-center">
              <Plus className="w-4 h-4 mr-1" />
              Add
            </button>
          </div>

          <div className="space-y-2">
            {transactions.map((transaction) => (
              <div
                key={transaction.id}
                className="flex justify-between p-3 border border-gray-200"
              >
                <div>
                  <p>{transaction.note}</p>
                  <p className="text-sm text-gray-500">{transaction.type}</p>
                </div>
                <p className={transaction.type === "Income" ? "text-green-600" : "text-red-600"}>
                  {transaction.type === "Income" ? "+" : "-"}${transaction.amount}
                </p>
              </div>
            ))}
          </div>
        </div>
      </div>

      {/* Bottom Navigation - positioned absolutely within the container */}
      <div className="absolute bottom-0 left-0 right-0 bg-white border-t border-gray-200">
        <div className="flex justify-around py-3">
          <div className="flex flex-col items-center text-gray-600">
            <BarChart3 className="w-6 h-6" />
            <span className="text-xs mt-1">Stats</span>
          </div>
          <div className="flex flex-col items-center text-gray-600">
            <CreditCard className="w-6 h-6" />
            <span className="text-xs mt-1">Budget</span>
          </div>
          <div className="flex flex-col items-center text-gray-600">
            <User className="w-6 h-6" />
            <span className="text-xs mt-1">Profile</span>
          </div>
        </div>
      </div>
    </div>
  );
}
