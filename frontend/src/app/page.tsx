"use client";

import React from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card";
import {
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer,
  LineChart, Line, AreaChart, Area
} from "recharts";
import {
  TrendingUp,
  Package,
  ShoppingCart,
  AlertCircle,
  ArrowUpRight,
  ArrowDownRight,
  Clock
} from "lucide-react";
import { Button } from "@/components/ui/Button";
import { cn } from "@/lib/utils";

const REVENUE_DATA = [
  { name: "Mon", momo: 4000, shopee: 2400, modian: 2400 },
  { name: "Tue", momo: 3000, shopee: 1398, modian: 2210 },
  { name: "Wed", momo: 2000, shopee: 9800, modian: 2290 },
  { name: "Thu", momo: 2780, shopee: 3908, modian: 2000 },
  { name: "Fri", momo: 1890, shopee: 4800, modian: 2181 },
  { name: "Sat", momo: 2390, shopee: 3800, modian: 2500 },
  { name: "Sun", momo: 3490, shopee: 4300, modian: 2100 },
];

const RECENT_ORDERS = [
  { id: "M001-8392", platform: "Momo", amount: "$1,299", status: "處理中", time: "10分鐘前" },
  { id: "S88-9921", platform: "Shopee", amount: "$450", status: "已完成", time: "1小時前" },
  { id: "MD+-1024", platform: "mo店+", amount: "$2,100", status: "待出貨", time: "2小時前" },
  { id: "M001-8391", platform: "Momo", amount: "$890", status: "已出貨", time: "昨天" },
];

export default function DashboardPage() {
  return (
    <div className="space-y-6 animate-in fade-in duration-500">
      <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
        <div>
          <h2 className="text-3xl font-bold tracking-tight">儀表板 (Dashboard)</h2>
          <p className="text-secondary-foreground mt-1">歡迎回來！這裡是您今日各平台的銷售總覽。</p>
        </div>
        <div className="flex items-center space-x-2">
          <Button variant="outline">下載報表</Button>
          <Button>同步全部平台資料</Button>
        </div>
      </div>

      {/* Stats row */}
      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-4">
        <Card className="bg-gradient-to-br from-card to-secondary/30 border-l-4 border-l-primary">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">總營業額</CardTitle>
            <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center">
              <TrendingUp className="w-4 h-4 text-primary" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">$45,231</div>
            <p className="text-xs text-secondary-foreground flex items-center mt-1">
              <span className="text-emerald-500 flex items-center mr-1"><ArrowUpRight className="w-3 h-3 mr-1" /> +20.1%</span>
              較上個月
            </p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-card to-secondary/30 border-l-4 border-l-emerald-500">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">今日訂單數</CardTitle>
            <div className="w-8 h-8 rounded-full bg-emerald-500/20 flex items-center justify-center">
              <ShoppingCart className="w-4 h-4 text-emerald-500" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">+125</div>
            <p className="text-xs text-secondary-foreground flex items-center mt-1">
              <span className="text-emerald-500 flex items-center mr-1"><ArrowUpRight className="w-3 h-3 mr-1" /> +12%</span>
              較昨天同時段
            </p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-card to-secondary/30 border-l-4 border-l-amber-500">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">待處理訂單</CardTitle>
            <div className="w-8 h-8 rounded-full bg-amber-500/20 flex items-center justify-center">
              <Clock className="w-4 h-4 text-amber-500" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">42</div>
            <p className="text-xs text-secondary-foreground mt-1">需要盡快安排出貨</p>
          </CardContent>
        </Card>

        <Card className="bg-gradient-to-br from-card to-secondary/30 border-l-4 border-l-rose-500">
          <CardHeader className="flex flex-row items-center justify-between space-y-0 pb-2">
            <CardTitle className="text-sm font-medium">庫存警告異常</CardTitle>
            <div className="w-8 h-8 rounded-full bg-rose-500/20 flex items-center justify-center">
              <AlertCircle className="w-4 h-4 text-rose-500" />
            </div>
          </CardHeader>
          <CardContent>
            <div className="text-2xl font-bold">7</div>
            <p className="text-xs text-secondary-foreground flex items-center mt-1">
              <span className="text-rose-500 font-medium">有商品已售完</span>
            </p>
          </CardContent>
        </Card>
      </div>

      <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-7">
        {/* Main Chart */}
        <Card className="col-span-4">
          <CardHeader>
            <CardTitle>過去一週各平台營收趨勢</CardTitle>
            <CardDescription>Momo, Shopee 與 mo店+ 的銷售對比</CardDescription>
          </CardHeader>
          <CardContent className="pl-0">
            <div className="h-[300px] w-full">
              <ResponsiveContainer width="100%" height="100%">
                <AreaChart data={REVENUE_DATA} margin={{ top: 10, right: 30, left: 0, bottom: 0 }}>
                  <defs>
                    <linearGradient id="colorMomo" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#ec4899" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#ec4899" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="colorShopee" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#f97316" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#f97316" stopOpacity={0} />
                    </linearGradient>
                    <linearGradient id="colorModian" x1="0" y1="0" x2="0" y2="1">
                      <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3} />
                      <stop offset="95%" stopColor="#3b82f6" stopOpacity={0} />
                    </linearGradient>
                  </defs>
                  <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                  <XAxis dataKey="name" axisLine={false} tickLine={false} tickMargin={10} />
                  <YAxis axisLine={false} tickLine={false} tickMargin={10} tickFormatter={(val) => `$${val}`} />
                  <Tooltip
                    contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }}
                  />
                  <Area type="monotone" dataKey="momo" stroke="#ec4899" strokeWidth={2} fillOpacity={1} fill="url(#colorMomo)" name="Momo購物" />
                  <Area type="monotone" dataKey="shopee" stroke="#f97316" strokeWidth={2} fillOpacity={1} fill="url(#colorShopee)" name="蝦皮購物" />
                  <Area type="monotone" dataKey="modian" stroke="#3b82f6" strokeWidth={2} fillOpacity={1} fill="url(#colorModian)" name="mo店+" />
                </AreaChart>
              </ResponsiveContainer>
            </div>
          </CardContent>
        </Card>

        {/* Recent Orders List */}
        <Card className="col-span-3">
          <CardHeader>
            <CardTitle>最新訂單動態</CardTitle>
            <CardDescription>各平台的即時訂單狀態</CardDescription>
          </CardHeader>
          <CardContent>
            <div className="space-y-4">
              {RECENT_ORDERS.map((order, i) => (
                <div key={i} className="flex items-center justify-between p-3 rounded-lg border border-border/50 bg-secondary/20 hover:bg-secondary/50 transition-colors">
                  <div className="flex items-center space-x-4">
                    <div className={cn(
                      "w-10 h-10 rounded-full flex items-center justify-center font-bold text-white",
                      order.platform === "Momo" ? "bg-pink-500" : order.platform === "Shopee" ? "bg-orange-500" : "bg-blue-500"
                    )}>
                      {order.platform[0]}
                    </div>
                    <div>
                      <p className="text-sm font-medium leading-none">{order.id}</p>
                      <p className="text-xs text-secondary-foreground mt-1">{order.platform} • {order.time}</p>
                    </div>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-bold">{order.amount}</p>
                    <div className={cn(
                      "inline-flex items-center rounded-full px-2.5 py-0.5 text-xs font-semibold mt-1",
                      order.status === "處理中" ? "bg-blue-100 text-blue-800" :
                        order.status === "待出貨" ? "bg-amber-100 text-amber-800" :
                          order.status === "已出貨" ? "bg-indigo-100 text-indigo-800" :
                            "bg-emerald-100 text-emerald-800"
                    )}>
                      {order.status}
                    </div>
                  </div>
                </div>
              ))}
            </div>
            <Button variant="outline" className="w-full mt-4">查看所有訂單</Button>
          </CardContent>
        </Card>
      </div>
    </div>
  );
}
