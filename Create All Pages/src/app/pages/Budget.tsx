import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { ArrowLeft, Plus } from "lucide-react";

interface BudgetCategory {
  id: string;
  category: string;
  limit: number;
  spent?: number;
}

export default function Budget() {
  const totalBudget = 5000;
  const categories: BudgetCategory[] = [
    { id: "1", category: "Food", limit: 500, spent: 300 },
    { id: "2", category: "Transport", limit: 200, spent: 150 },
    { id: "3", category: "Entertainment", limit: 300, spent: 200 },
    { id: "4", category: "Utilities", limit: 400, spent: 350 },
  ];

  const totalPlanned = categories.reduce((sum, cat) => sum + cat.limit, 0);

  return (
    <div className="min-h-full bg-gray-50 pb-20">
      <div className="w-full p-4">
        <div className="flex items-center gap-3 mb-6 pt-4">
          <button className="h-10 w-10 inline-flex items-center justify-center rounded-md">
            <ArrowLeft className="w-6 h-6" />
          </button>
          <h1 className="text-2xl">Budget</h1>
        </div>

        {/* Total Budget */}
        <div className="bg-white border border-gray-200 p-4 mb-4 text-center">
          <p className="text-sm text-gray-600 mb-2">Total Budget</p>
          <p className="text-3xl text-blue-600">${totalBudget}</p>
        </div>

        {/* Planned Budget Summary */}
        <div className="bg-white border border-gray-200 p-4 mb-4">
          <h2 className="text-lg mb-3">Planned Budget</h2>
          <div className="space-y-2">
            <div className="flex justify-between">
              <span className="text-gray-600">Total Planned:</span>
              <span>${totalPlanned}</span>
            </div>
            <div className="flex justify-between">
              <span className="text-gray-600">Remaining:</span>
              <span className={totalBudget - totalPlanned >= 0 ? "text-green-600" : "text-red-600"}>
                ${totalBudget - totalPlanned}
              </span>
            </div>
          </div>
        </div>

        {/* Categories */}
        <div className="bg-white border border-gray-200 p-4 mb-4">
          <div className="flex justify-between items-center mb-3">
            <h2 className="text-lg">Categories</h2>
            <button className="h-9 px-4 bg-blue-600 text-white rounded-md text-sm inline-flex items-center">
              <Plus className="w-4 h-4 mr-1" />
              Add
            </button>
          </div>

          <div className="space-y-3">
            {categories.map((category) => (
              <div key={category.id} className="p-3 border border-gray-200">
                <div className="flex justify-between mb-2">
                  <span>{category.category}</span>
                  <span className="text-blue-600">${category.limit}</span>
                </div>
                {category.spent !== undefined && (
                  <div className="flex justify-between text-sm text-gray-600">
                    <span>Spent: ${category.spent}</span>
                    <span>{((category.spent / category.limit) * 100).toFixed(0)}%</span>
                  </div>
                )}
              </div>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}