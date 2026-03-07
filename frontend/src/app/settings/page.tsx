"use client";

import React from "react";
import { Card, CardHeader, CardTitle, CardDescription, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";

export default function SettingsPage() {
    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            <div>
                <h2 className="text-3xl font-bold tracking-tight">系統設定</h2>
                <p className="text-secondary-foreground mt-1">管理您的帳號資訊、API 金鑰與爬蟲設定。</p>
            </div>

            <div className="grid gap-6 max-w-3xl">
                <Card>
                    <CardHeader>
                        <CardTitle>Momo 爬蟲設定</CardTitle>
                        <CardDescription>設定 Playwright 爬蟲在 Momo 購物的登入憑證。</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <label className="text-sm font-medium">帳號 (User ID)</label>
                            <input type="text" className="w-full px-3 py-2 bg-secondary border border-border rounded-md text-sm outline-none focus:ring-1 focus:ring-primary" placeholder="輸入 Momo 商店帳號" />
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium">密碼 (Password)</label>
                            <input type="password" className="w-full px-3 py-2 bg-secondary border border-border rounded-md text-sm outline-none focus:ring-1 focus:ring-primary" placeholder="••••••••" />
                        </div>
                        <div className="pt-4 flex justify-end">
                            <Button>儲存連線設定</Button>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>mo店+ 爬蟲設定</CardTitle>
                        <CardDescription>設定 Playwright 爬蟲在 mo店+ 的登入憑證。</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <label className="text-sm font-medium">帳號 (User ID)</label>
                            <input type="text" className="w-full px-3 py-2 bg-secondary border border-border rounded-md text-sm outline-none focus:ring-1 focus:ring-primary" placeholder="輸入 mo店+ 商家帳號" />
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium">密碼 (Password)</label>
                            <input type="password" className="w-full px-3 py-2 bg-secondary border border-border rounded-md text-sm outline-none focus:ring-1 focus:ring-primary" placeholder="••••••••" />
                        </div>
                        <div className="pt-4 flex justify-end">
                            <Button>儲存連線設定</Button>
                        </div>
                    </CardContent>
                </Card>

                <Card>
                    <CardHeader>
                        <CardTitle>蝦皮 (Shopee) 爬蟲設定</CardTitle>
                        <CardDescription>設定蝦皮賣家中心的登入連線資訊。</CardDescription>
                    </CardHeader>
                    <CardContent className="space-y-4">
                        <div className="space-y-2">
                            <label className="text-sm font-medium">賣家帳號</label>
                            <input type="text" className="w-full px-3 py-2 bg-secondary border border-border rounded-md text-sm outline-none focus:ring-1 focus:ring-primary" placeholder="輸入 Shopee 帳號" />
                        </div>
                        <div className="space-y-2">
                            <label className="text-sm font-medium">密碼</label>
                            <input type="password" className="w-full px-3 py-2 bg-secondary border border-border rounded-md text-sm outline-none focus:ring-1 focus:ring-primary" placeholder="••••••••" />
                        </div>
                        <div className="pt-4 flex justify-end">
                            <Button>儲存連線設定</Button>
                        </div>
                    </CardContent>
                </Card>
            </div>
        </div>
    );
}
