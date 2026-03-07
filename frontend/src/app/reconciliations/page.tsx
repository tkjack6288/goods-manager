"use client";

import React, { useState } from "react";
import { Card, CardContent, CardHeader, CardTitle, CardDescription } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Download, FileText, Calculator } from "lucide-react";
import {
    BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, Legend
} from "recharts";
import { cn } from "@/lib/utils";

const DATA = [
    { platform: "Momo", revenue: 15400, fee: 1200, shipping: 300, net: 13900 },
    { platform: "Shopee", revenue: 9800, fee: 882, shipping: 150, net: 8768 },
    { platform: "mo店+", revenue: 12500, fee: 1000, shipping: 250, net: 11250 },
];

export default function ReconciliationsPage() {
    const [selectedMonth, setSelectedMonth] = useState("2026-02");

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight">對帳報表</h2>
                    <p className="text-secondary-foreground mt-1">結算各平台營業額、扣除手續費及運費的淨利潤。</p>
                </div>
                <div className="flex items-center space-x-2">
                    <input
                        type="month"
                        value={selectedMonth}
                        onChange={(e) => setSelectedMonth(e.target.value)}
                        className="px-3 py-2 bg-secondary border border-border rounded-md text-sm outline-none focus:ring-1 focus:ring-primary"
                    />
                    <Button variant="outline"><Calculator className="w-4 h-4 mr-2" /> 重新計算</Button>
                    <Button><Download className="w-4 h-4 mr-2" /> 下載月結表</Button>
                </div>
            </div>

            <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
                <Card className="bg-gradient-to-br from-card to-secondary/30">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium">總結算金額 (Gross Revenue)</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-3xl font-bold">$37,700</div>
                    </CardContent>
                </Card>
                <Card className="bg-gradient-to-br from-card to-secondary/30">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium">平台與運費扣減 (Total Deductions)</CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-3xl font-bold text-rose-500">-$3,782</div>
                    </CardContent>
                </Card>
                <Card className="bg-gradient-to-br from-card to-secondary/30 border-t-4 border-t-primary shadow-md">
                    <CardHeader className="pb-2">
                        <CardTitle className="text-sm font-medium flex items-center">
                            實收淨利 (Net Income) <span className="ml-2 text-xs bg-primary/20 text-primary px-2 py-0.5 rounded-full">已結算</span>
                        </CardTitle>
                    </CardHeader>
                    <CardContent>
                        <div className="text-4xl font-black text-primary">$33,918</div>
                    </CardContent>
                </Card>
            </div>

            <div className="grid grid-cols-1 lg:grid-cols-2 gap-4">
                <Card>
                    <CardHeader>
                        <CardTitle>平台淨收益對比圖</CardTitle>
                        <CardDescription>{selectedMonth} 單月結算數據</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="h-[300px] w-full">
                            <ResponsiveContainer width="100%" height="100%">
                                <BarChart data={DATA} margin={{ top: 20, right: 30, left: 20, bottom: 5 }}>
                                    <CartesianGrid strokeDasharray="3 3" vertical={false} stroke="#e2e8f0" />
                                    <XAxis dataKey="platform" axisLine={false} tickLine={false} />
                                    <YAxis axisLine={false} tickLine={false} tickFormatter={(val) => `$${val}`} />
                                    <Tooltip cursor={{ fill: 'transparent' }} contentStyle={{ borderRadius: '8px', border: 'none', boxShadow: '0 4px 6px -1px rgb(0 0 0 / 0.1)' }} />
                                    <Legend />
                                    <Bar dataKey="revenue" name="營業額" fill="#94a3b8" radius={[4, 4, 0, 0]} />
                                    <Bar dataKey="net" name="實收淨利" fill="#3b82f6" radius={[4, 4, 0, 0]} />
                                </BarChart>
                            </ResponsiveContainer>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>月度結算明細</CardTitle>
                        <CardDescription>各平台詳細分項數據</CardDescription>
                    </CardHeader>
                    <CardContent>
                        <div className="rounded-md border border-border overflow-hidden">
                            <table className="w-full text-sm text-left">
                                <thead className="bg-secondary text-secondary-foreground font-medium uppercase text-xs border-b border-border">
                                    <tr>
                                        <th className="px-4 py-3">平台</th>
                                        <th className="px-4 py-3 text-right">營業額</th>
                                        <th className="px-4 py-3 text-right">手續費</th>
                                        <th className="px-4 py-3 text-right">運費扣抵</th>
                                        <th className="px-4 py-3 text-right">本期淨利</th>
                                    </tr>
                                </thead>
                                <tbody className="divide-y divide-border">
                                    {DATA.map((row, i) => (
                                        <tr key={i} className="hover:bg-secondary/30 transition-colors">
                                            <td className="px-4 py-4 font-medium flex items-center">
                                                <FileText className="w-4 h-4 mr-2 text-primary" />
                                                {row.platform}
                                            </td>
                                            <td className="px-4 py-4 text-right">${row.revenue.toLocaleString()}</td>
                                            <td className="px-4 py-4 text-right text-rose-500">-${row.fee.toLocaleString()}</td>
                                            <td className="px-4 py-4 text-right text-rose-500">-${row.shipping.toLocaleString()}</td>
                                            <td className="px-4 py-4 text-right font-bold text-primary">${row.net.toLocaleString()}</td>
                                        </tr>
                                    ))}
                                    <tr className="bg-secondary/30 font-bold border-t-2 border-border">
                                        <td className="px-4 py-4">總計</td>
                                        <td className="px-4 py-4 text-right">$37,700</td>
                                        <td className="px-4 py-4 text-right text-rose-500">-$3,082</td>
                                        <td className="px-4 py-4 text-right text-rose-500">-$700</td>
                                        <td className="px-4 py-4 text-right text-xl text-primary">$33,918</td>
                                    </tr>
                                </tbody>
                            </table>
                        </div>
                        <div className="flex justify-end mt-4">
                            <Button variant="outline" size="sm">檢視詳細交易紀錄</Button>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
