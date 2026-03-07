"use client";

import React, { useState } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Plus, Search, Filter, RefreshCw, MoreHorizontal, Check, X } from "lucide-react";

// Mock data
const PRODUCTS = [
    { id: "P001", sku: "S-502-B", name: "無線降噪藍牙耳機 黑", price: 2990, stock: 45, momo: true, shopee: true, modian: false },
    { id: "P002", sku: "S-502-W", name: "無線降噪藍牙耳機 白", price: 2990, stock: 12, momo: true, shopee: true, modian: true },
    { id: "P003", sku: "T-098-G", name: "多功能快充行動電源 10000mAh", price: 890, stock: 0, momo: false, shopee: true, modian: false },
    { id: "P004", sku: "K-112-Q", name: "機械式電競鍵盤 RGB", price: 1450, stock: 8, momo: true, shopee: false, modian: true },
    { id: "P005", sku: "M-403-1", name: "人體工學無線滑鼠", price: 799, stock: 120, momo: true, shopee: true, modian: true },
];

export default function ProductsPage() {
    const [searchTerm, setSearchTerm] = useState("");
    const [isSyncing, setIsSyncing] = useState(false);

    const handleSync = async () => {
        setIsSyncing(true);
        try {
            const res = await fetch("https://goods-manager-backend-164815154526.asia-east1.run.app/api/platforms/sync/products/", {
                method: "POST"
            });
            if (res.ok) {
                alert("已在背景觸發商品同步任務！這可能需要幾分鐘的時間，請稍後重整查看最新狀態。");
            } else {
                alert("同步請求失敗，請確認後端是否正常運作。");
            }
        } catch (error) {
            console.error("同步錯誤:", error);
            alert("網路錯誤，無法連線至後端伺服器。");
        } finally {
            setIsSyncing(false);
        }
    };

    const filteredProducts = PRODUCTS.filter(p =>
        p.name.includes(searchTerm) || p.sku.includes(searchTerm)
    );

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight">商品管理</h2>
                    <p className="text-secondary-foreground mt-1">管理各平台商品、價格與庫存狀態。</p>
                </div>
                <div className="flex items-center space-x-2">
                    <Button variant="outline" onClick={handleSync} disabled={isSyncing}>
                        <RefreshCw className={`w-4 h-4 mr-2 ${isSyncing ? "animate-spin" : ""}`} />
                        {isSyncing ? "同步中..." : "全部同步"}
                    </Button>
                    <Button><Plus className="w-4 h-4 mr-2" /> 新增商品</Button>
                </div>
            </div>

            <Card>
                <CardHeader className="pb-4">
                    <div className="flex flex-col sm:flex-row justify-between gap-4">
                        <div className="relative max-w-sm w-full">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-secondary-foreground" />
                            <input
                                placeholder="搜尋商品名稱或 SKU..."
                                value={searchTerm}
                                onChange={(e) => setSearchTerm(e.target.value)}
                                className="w-full pl-9 pr-4 py-2 bg-secondary border border-border rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary"
                            />
                        </div>
                        <div className="flex gap-2">
                            <Button variant="outline" size="sm">
                                <Filter className="w-4 h-4 mr-2" />
                                進階篩選
                            </Button>
                        </div>
                    </div>
                </CardHeader>
                <CardContent>
                    <div className="rounded-md border border-border overflow-x-auto">
                        <table className="w-full text-sm text-left">
                            <thead className="bg-secondary text-secondary-foreground font-medium uppercase text-xs border-b border-border">
                                <tr>
                                    <th className="px-4 py-3">商品圖片 / 名稱</th>
                                    <th className="px-4 py-3">SKU</th>
                                    <th className="px-4 py-3">定價</th>
                                    <th className="px-4 py-3">總庫存</th>
                                    <th className="px-4 py-3 text-center">Momo</th>
                                    <th className="px-4 py-3 text-center">蝦皮</th>
                                    <th className="px-4 py-3 text-center">mo店+</th>
                                    <th className="px-4 py-3 text-right">操作</th>
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-border">
                                {filteredProducts.map((product) => (
                                    <tr key={product.id} className="hover:bg-secondary/30 transition-colors">
                                        <td className="px-4 py-4">
                                            <div className="flex items-center space-x-3">
                                                <div className="w-10 h-10 rounded bg-secondary flex items-center justify-center text-secondary-foreground shrink-0 border border-border">
                                                    {/* Placeholder Image */}
                                                    <svg className="w-5 h-5 opacity-50" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                                                        <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16l4.586-4.586a2 2 0 012.828 0L16 16m-2-2l1.586-1.586a2 2 0 012.828 0L20 14m-6-6h.01M6 20h12a2 2 0 002-2V6a2 2 0 00-2-2H6a2 2 0 00-2 2v12a2 2 0 002 2z" />
                                                    </svg>
                                                </div>
                                                <div className="font-medium">{product.name}</div>
                                            </div>
                                        </td>
                                        <td className="px-4 py-4 text-secondary-foreground font-mono text-xs">{product.sku}</td>
                                        <td className="px-4 py-4">${product.price.toLocaleString()}</td>
                                        <td className="px-4 py-4">
                                            <span className={product.stock === 0 ? "text-rose-500 font-bold" : product.stock < 10 ? "text-amber-500 font-bold" : ""}>
                                                {product.stock}
                                            </span>
                                        </td>
                                        <td className="px-4 py-4 text-center">
                                            <div className="flex justify-center">
                                                {product.momo ? <Check className="w-5 h-5 text-emerald-500" /> : <X className="w-5 h-5 text-rose-500/50" />}
                                            </div>
                                        </td>
                                        <td className="px-4 py-4 text-center">
                                            <div className="flex justify-center">
                                                {product.shopee ? <Check className="w-5 h-5 text-emerald-500" /> : <X className="w-5 h-5 text-rose-500/50" />}
                                            </div>
                                        </td>
                                        <td className="px-4 py-4 text-center">
                                            <div className="flex justify-center">
                                                {product.modian ? <Check className="w-5 h-5 text-emerald-500" /> : <X className="w-5 h-5 text-rose-500/50" />}
                                            </div>
                                        </td>
                                        <td className="px-4 py-4 text-right">
                                            <Button variant="ghost" size="icon">
                                                <MoreHorizontal className="w-4 h-4 text-secondary-foreground" />
                                            </Button>
                                        </td>
                                    </tr>
                                ))}
                                {filteredProducts.length === 0 && (
                                    <tr>
                                        <td colSpan={8} className="px-4 py-8 text-center text-secondary-foreground">
                                            找不到符合條件的商品
                                        </td>
                                    </tr>
                                )}
                            </tbody>
                        </table>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}
