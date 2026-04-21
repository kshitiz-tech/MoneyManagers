import { Tabs, TabsContent, TabsList, TabsTrigger } from "../components/ui/tabs";
import { ArrowLeft } from "lucide-react";
import { PieChart, Pie, Cell, ResponsiveContainer, Tooltip } from "recharts";

export default function Stats() {
  const activeTab = "income";

  // Mock data for income categories
  const incomeData = [
    { name: "Salary", value: 5000, color: "#10b981" },
    { name: "Freelance", value: 1500, color: "#3b82f6" },
    { name: "Investments", value: 800, color: "#8b5cf6" },
    { name: "Other", value: 200, color: "#f59e0b" },
  ];

  // Mock data for expense categories
  const expenseData = [
    { name: "Rent", value: 1200, color: "#ef4444" },
    { name: "Food", value: 600, color: "#f97316" },
    { name: "Transport", value: 300, color: "#eab308" },
    { name: "Entertainment", value: 250, color: "#ec4899" },
    { name: "Utilities", value: 200, color: "#8b5cf6" },
    { name: "Shopping", value: 400, color: "#06b6d4" },
    { name: "Other", value: 150, color: "#84cc16" },
  ];

  const totalIncome = incomeData.reduce((sum, item) => sum + item.value, 0);
  const totalExpense = expenseData.reduce((sum, item) => sum + item.value, 0);

  const renderChart = (data: typeof incomeData, total: number) => (
    <div className="space-y-4">
      <ResponsiveContainer width="100%" height={280}>
        <PieChart>
          <Pie
            data={data}
            cx="50%"
            cy="50%"
            labelLine={false}
            label={({ name, percent }) => `${name} ${(percent * 100).toFixed(0)}%`}
            outerRadius={90}
            fill="#8884d8"
            dataKey="value"
            isAnimationActive={false}
          >
            {data.map((entry, index) => (
              <Cell key={`cell-${index}`} fill={entry.color} />
            ))}
          </Pie>
          <Tooltip formatter={(value: number) => `$${value.toFixed(2)}`} />
        </PieChart>
      </ResponsiveContainer>

      <div className="space-y-2">
        {data.map((item, index) => (
          <div key={index} className="flex justify-between p-3 border border-gray-200">
            <div className="flex items-center gap-3">
              <div
                className="w-4 h-4"
                style={{ backgroundColor: item.color }}
              ></div>
              <span>{item.name}</span>
            </div>
            <div className="text-right">
              <p>${item.value}</p>
              <p className="text-sm text-gray-600">
                {((item.value / total) * 100).toFixed(1)}%
              </p>
            </div>
          </div>
        ))}
      </div>

      <div className="p-3 bg-gray-100 border border-gray-200">
        <div className="flex justify-between">
          <span>Total:</span>
          <span className="text-xl text-blue-600">${total}</span>
        </div>
      </div>
    </div>
  );

  return (
    <div className="min-h-full bg-gray-50 pb-20">
      <div className="w-full p-4">
        <div className="flex items-center gap-3 mb-6 pt-4">
          <button className="h-10 w-10 inline-flex items-center justify-center rounded-md">
            <ArrowLeft className="w-6 h-6" />
          </button>
          <h1 className="text-2xl">Statistics</h1>
        </div>

        <div className="bg-white border border-gray-200 p-4">
          <h2 className="text-lg mb-4">Financial Overview</h2>

          <Tabs value={activeTab}>
            <TabsList className="grid w-full grid-cols-2 h-11">
              <TabsTrigger value="income">Income</TabsTrigger>
              <TabsTrigger value="expense">Expense</TabsTrigger>
            </TabsList>
            <TabsContent value="income" className="mt-4">
              {renderChart(incomeData, totalIncome)}
            </TabsContent>
            <TabsContent value="expense" className="mt-4">
              {renderChart(expenseData, totalExpense)}
            </TabsContent>
          </Tabs>
        </div>
      </div>
    </div>
  );
}