import { Input } from "../components/ui/input";
import { Label } from "../components/ui/label";
import { Select, SelectContent, SelectItem, SelectTrigger, SelectValue } from "../components/ui/select";
import { Textarea } from "../components/ui/textarea";
import { ArrowLeft } from "lucide-react";

export default function Transaction() {
  const amount = "1200";
  const type = "Expense";
  const date = "2024-03-02";
  const note = "Rent";

  return (
    <div className="min-h-full bg-gray-50">
      <div className="w-full p-4">
        <div className="flex items-center gap-3 mb-6 pt-4">
          <button className="h-10 w-10 inline-flex items-center justify-center rounded-md">
            <ArrowLeft className="w-6 h-6" />
          </button>
          <h1 className="text-2xl">Update Transaction</h1>
        </div>

        <div className="bg-white border border-gray-200 p-4">
          <h2 className="text-lg mb-4">Transaction Details</h2>

          <form className="space-y-4">
            <div>
              <Label htmlFor="amount">Amount</Label>
              <Input
                id="amount"
                type="number"
                step="0.01"
                value={amount}
                placeholder="0.00"
                className="h-12 mt-1"
              />
            </div>

            <div>
              <Label htmlFor="type">Type</Label>
              <Select value={type}>
                <SelectTrigger id="type" className="h-12 mt-1">
                  <SelectValue />
                </SelectTrigger>
                <SelectContent>
                  <SelectItem value="Income">Income</SelectItem>
                  <SelectItem value="Expense">Expense</SelectItem>
                </SelectContent>
              </Select>
            </div>

            <div>
              <Label htmlFor="date">Date</Label>
              <Input
                id="date"
                type="date"
                value={date}
                className="h-12 mt-1"
              />
            </div>

            <div>
              <Label htmlFor="note">Note</Label>
              <Textarea
                id="note"
                value={note}
                placeholder="Add a note..."
                className="mt-1"
                rows={3}
              />
            </div>

            <button type="button" className="w-full h-12 bg-blue-600 text-white rounded-md">
              Save
            </button>
          </form>
        </div>
      </div>
    </div>
  );
}
