"use client";

import React, { useState, useEffect } from "react";
import { Card, CardHeader, CardTitle, CardContent } from "@/components/ui/Card";
import { Button } from "@/components/ui/Button";
import { Download, Search, RefreshCw, Eye } from "lucide-react";
import { cn } from "@/lib/utils";

// 宣告訂單介面
interface Order {
    id: number;
    platform: string;
    platform_order_id: string;
    total_amount: number;
    status: string;
    order_date: string;
    customer_info?: any;
    items?: any[];
    platform_details?: any;
}

export default function OrdersPage() {
    const [isSyncing, setIsSyncing] = useState(false);
    const [orders, setOrders] = useState<Order[]>([]);
    const [isLoading, setIsLoading] = useState(true);

    const [searchQuery, setSearchQuery] = useState("");
    const [selectedPlatform, setSelectedPlatform] = useState("全部平台");
    const [selectedStatus, setSelectedStatus] = useState("全部狀態");

    const fetchOrders = async () => {
        setIsLoading(true);
        try {
            const params = new URLSearchParams();
            if (searchQuery) params.append("search", searchQuery);
            if (selectedPlatform && selectedPlatform !== "全部平台") params.append("platform", selectedPlatform);
            if (selectedStatus && selectedStatus !== "全部狀態") params.append("status", selectedStatus);

            const res = await fetch(`http://localhost:8000/api/orders?${params.toString()}`);
            if (res.ok) {
                const data = await res.json();
                setOrders(data);
            }
        } catch (error) {
            console.error("無法取得訂單資料:", error);
        } finally {
            setIsLoading(false);
        }
    };

    useEffect(() => {
        const timer = setTimeout(() => {
            fetchOrders();
        }, 300);
        return () => clearTimeout(timer);
    }, [searchQuery, selectedPlatform, selectedStatus]);

    const handleSync = async (platform?: string) => {
        setIsSyncing(true);
        try {
            const url = platform ? `http://localhost:8000/api/platforms/sync/orders?platform=${platform}` : "http://localhost:8000/api/platforms/sync/orders";
            const res = await fetch(url, {
                method: "POST"
            });
            if (res.ok) {
                alert("已在背景觸發訂單同步任務！這可能需要幾分鐘的時間，請稍後重整查看最新狀態。");
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

    const columns = [
        "訂單編號", "配送狀態", "配送訊息", "指定配送日", "物流公司",
        "配送單號", "出貨包材", "包材類型", "包材重量", "訂單類別",
        "客戶配送需求", "發票開立統編", "廢四機回收", "轉單日", "最晚出貨日",
        "收件人姓名", "電話", "地址", "商品原廠編號", "商品編號",
        "商品名稱", "單品規格", "數量", "訂單金額", "商品屬性",
        "應稅(免稅)", "發票開立金額", "訂購人姓名"
    ];

    return (
        <div className="space-y-6 animate-in fade-in duration-500">
            <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                <div>
                    <h2 className="text-3xl font-bold tracking-tight">訂單管理</h2>
                    <p className="text-secondary-foreground mt-1">來自各平台的訂單集中檢視與狀態更新。</p>
                </div>
                <div className="flex items-center space-x-2">
                    <Button variant="outline"><Download className="w-4 h-4 mr-2" /> 匯出 CSV</Button>
                    <Button variant="outline" onClick={() => handleSync("modian")} disabled={isSyncing} className="border-blue-200 text-blue-700 hover:bg-blue-50">
                        <RefreshCw className={`w-4 h-4 mr-2 ${isSyncing ? "animate-spin" : ""}`} />
                        同步 mo店+
                    </Button>
                    <Button onClick={() => handleSync()} disabled={isSyncing}>
                        <RefreshCw className={`w-4 h-4 mr-2 ${isSyncing ? "animate-spin" : ""}`} />
                        {isSyncing ? "同步中..." : "全部同步"}
                    </Button>
                </div>
            </div>

            <Card>
                <CardHeader className="pb-4">
                    <div className="flex flex-col sm:flex-row justify-between gap-4">
                        <div className="relative max-w-sm w-full">
                            <Search className="absolute left-3 top-1/2 -translate-y-1/2 h-4 w-4 text-secondary-foreground" />
                            <input
                                placeholder="搜尋訂單編號或買家名稱..."
                                className="w-full pl-9 pr-4 py-2 bg-secondary border border-border rounded-md text-sm focus:outline-none focus:ring-1 focus:ring-primary"
                                value={searchQuery}
                                onChange={(e) => setSearchQuery(e.target.value)}
                            />
                        </div>
                        <div className="flex space-x-2">
                            <select
                                className="bg-secondary border border-border rounded-md text-sm p-2 outline-none"
                                value={selectedPlatform}
                                onChange={(e) => setSelectedPlatform(e.target.value)}
                            >
                                <option>全部平台</option>
                                <option>Momo</option>
                                <option>Shopee</option>
                                <option>mo店+</option>
                            </select>
                            <select
                                className="bg-secondary border border-border rounded-md text-sm p-2 outline-none"
                                value={selectedStatus}
                                onChange={(e) => setSelectedStatus(e.target.value)}
                            >
                                <option>全部狀態</option>
                                <option>請回覆</option>
                                <option>待進貨</option>
                                <option>待出貨</option>
                                <option>客戶取消訂單</option>
                                <option>無貨取消訂單</option>
                                <option>已取消</option>
                                <option>已出貨</option>
                                <option>客戶申請退貨</option>
                            </select>
                            <div className="flex items-center text-sm font-medium text-muted-foreground ml-2 px-2 bg-secondary/50 rounded-md border border-border border-dashed">
                                查詢結果：<span className="text-primary font-bold mx-1">{orders.length}</span> 筆
                            </div>
                        </div>
                    </div>
                </CardHeader>
                <CardContent>
                    <div className="rounded-md border border-border overflow-x-auto">
                        <table className="w-max text-sm text-left whitespace-nowrap">
                            <thead className="bg-secondary text-secondary-foreground font-medium uppercase text-xs border-b border-border">
                                <tr>
                                    <th className="px-4 py-3 sticky left-0 bg-secondary z-10 border-r border-border shadow-[1px_0_0_0_#e5e7eb] text-center w-12">序號</th>
                                    <th className="px-4 py-3 sticky left-[3rem] bg-secondary z-10 border-r border-border shadow-[1px_0_0_0_#e5e7eb]">處理狀態</th>
                                    <th className="px-4 py-3 sticky left-[11rem] bg-secondary z-10 border-r border-border shadow-[1px_0_0_0_#e5e7eb]">平台</th>
                                    {columns.map(col => (
                                        <th key={col} className="px-4 py-3 whitespace-nowrap">{col}</th>
                                    ))}
                                </tr>
                            </thead>
                            <tbody className="divide-y divide-border">
                                {isLoading ? (
                                    <tr>
                                        <td colSpan={columns.length + 4} className="px-4 py-8 text-center text-secondary-foreground">載入中...</td>
                                    </tr>
                                ) : orders.length === 0 ? (
                                    <tr>
                                        <td colSpan={columns.length + 4} className="px-4 py-8 text-center text-secondary-foreground">目前沒有任何訂單資料。請點擊「同步最新訂單」。</td>
                                    </tr>
                                ) : (
                                    orders.map((order, index) => {
                                        const pd = order.platform_details || {};

                                        // 映射各欄位資料，若從 platform_details 中找不到，則使用 order 本身的欄位或空字串
                                        const getField = (colName: string) => {
                                            if (colName === "訂單編號") return pd["訂單編號"] || order.platform_order_id || "-";
                                            if (colName === "配送狀態") return pd["配送狀態"] || order.status || "-";
                                            if (colName === "配送訊息") return pd["配送訊息"] || "-";
                                            if (colName === "指定配送日") return pd["指定配送日"] || "-";
                                            if (colName === "物流公司") return pd["物流公司"] || "-";
                                            if (colName === "配送單號") return pd["配送單號"] || "-";
                                            if (colName === "出貨包材") return pd["出貨包材"] || "-";
                                            if (colName === "包材類型") return pd["包材類型"] || "-";
                                            if (colName === "包材重量") return pd["包材重量"] || "-";
                                            if (colName === "訂單類別") return pd["訂單類別"] || "-";
                                            if (colName === "客戶配送需求") return pd["客戶配送需求"] || "-";
                                            if (colName === "發票開立統編") return pd["發票開立統編"] || "-";
                                            if (colName === "廢四機回收") return pd["廢四機回收"] || "-";
                                            if (colName === "轉單日") return pd["轉單日"] || "-";
                                            if (colName === "最晚出貨日") return pd["最晚出貨日"] || "-";
                                            if (colName === "收件人姓名") return pd["收件人姓名"] || order.customer_info?.name || "-";
                                            if (colName === "電話") return pd["電話"] || order.customer_info?.phone || "-";
                                            if (colName === "地址") return pd["地址"] || order.customer_info?.address || "-";
                                            if (colName === "商品原廠編號") return pd["商品原廠編號"] || "-";
                                            if (colName === "商品編號") return pd["商品編號"] || "-";
                                            if (colName === "商品名稱") return pd["商品名稱"] || (order.items && order.items.length > 0 ? order.items[0]?.product_name : "-");
                                            if (colName === "單品規格") return pd["單品規格"] || "-";
                                            if (colName === "數量") return pd["數量"] || (order.items && order.items.length > 0 ? order.items[0]?.quantity : "-");
                                            if (colName === "訂單金額") return pd["訂單金額"] || order.total_amount || "-";
                                            if (colName === "商品屬性") return pd["商品屬性"] || "-";
                                            if (colName === "應稅(免稅)") return pd["應稅(免稅)"] || pd["應稅免稅"] || "-";
                                            if (colName === "發票開立金額") return pd["發票開立金額"] || "-";
                                            if (colName === "訂購人姓名") return pd["訂購人姓名"] || "-";
                                            return "-";
                                        };

                                        // 更新訂單狀態的 API 呼叫
                                        const updateOrderStatus = async (newStatus: string) => {
                                            try {
                                                const res = await fetch(`http://localhost:8000/api/orders/${order.id}/status`, {
                                                    method: "PATCH",
                                                    headers: { "Content-Type": "application/json" },
                                                    body: JSON.stringify({ status: newStatus })
                                                });
                                                if (res.ok) {
                                                    // 更新成本地 state 以即時反映畫面 (包含連動運費的重整)
                                                    fetchOrders();
                                                } else {
                                                    alert("狀態更新失敗");
                                                }
                                            } catch (error) {
                                                console.error("狀態更新錯誤:", error);
                                            }
                                        };

                                        const productName = getField("商品名稱");
                                        const isShippingFee = productName === "運費";

                                        return (
                                            <tr key={order.id} className="hover:bg-secondary/30 transition-colors">
                                                <td className="px-4 py-4 sticky left-0 bg-background z-10 border-r border-border shadow-[1px_0_0_0_#e5e7eb] text-center text-muted-foreground font-medium w-12 text-xs">
                                                    {index + 1}
                                                </td>
                                                <td className="px-4 py-4 sticky left-[3rem] bg-background z-20 border-r border-border shadow-[1px_0_0_0_#e5e7eb]">
                                                    {isShippingFee ? (
                                                        <span className={cn(
                                                            "inline-flex items-center rounded-sm px-2 py-0.5 text-xs font-semibold",
                                                            order.status.includes("請回覆") ? "bg-red-50 text-red-700 border border-red-200" :
                                                                order.status.includes("待進貨") ? "bg-teal-50 text-teal-700 border border-teal-200" :
                                                                    order.status.includes("待出貨") ? "bg-amber-50 text-amber-700 border border-amber-200" :
                                                                        order.status.includes("取消") || order.status.includes("退") ? "bg-rose-50 text-rose-700 border border-rose-200" :
                                                                            order.status.includes("已出貨") || order.status.includes("配送") ? "bg-indigo-50 text-indigo-700 border border-indigo-200" :
                                                                                "bg-secondary/50 text-secondary-foreground border border-transparent"
                                                        )}>
                                                            {order.status}
                                                        </span>
                                                    ) : (
                                                        <select
                                                            className={cn(
                                                                "bg-transparent border border-border rounded-md text-xs p-1 outline-none font-semibold",
                                                                order.status.includes("請回覆") ? "text-red-700 bg-red-50 border-red-200" :
                                                                    order.status.includes("待進貨") ? "text-teal-700 bg-teal-50 border-teal-200" :
                                                                        order.status.includes("待出貨") ? "text-amber-700 bg-amber-50 border-amber-200" :
                                                                            order.status.includes("取消") || order.status.includes("退") ? "text-rose-700 bg-rose-50 border-rose-200" :
                                                                                order.status.includes("已出貨") || order.status.includes("配送") ? "text-indigo-700 bg-indigo-50 border-indigo-200" :
                                                                                    "text-secondary-foreground"
                                                            )}
                                                            value={order.status}
                                                            onChange={(e) => updateOrderStatus(e.target.value)}
                                                        >
                                                            <option value="請回覆">請回覆</option>
                                                            <option value="待進貨">待進貨</option>
                                                            <option value="待出貨">待出貨</option>
                                                            <option value="客戶取消訂單">客戶取消訂單</option>
                                                            <option value="無貨取消訂單">無貨取消訂單</option>
                                                            <option value="已取消">已取消</option>
                                                            <option value="已出貨">已出貨</option>
                                                            <option value="客戶申請退貨">客戶申請退貨</option>
                                                            <option value={order.status} disabled hidden>{order.status}</option>
                                                        </select>
                                                    )}
                                                </td>
                                                <td className="px-4 py-4 sticky left-[11rem] bg-background z-20 border-r border-border shadow-[1px_0_0_0_#e5e7eb]">
                                                    <span className={cn(
                                                        "inline-flex items-center rounded-sm px-2 py-0.5 text-xs font-semibold",
                                                        (order.platform || "").includes("Momo") ? "bg-pink-100 text-pink-800" :
                                                            (order.platform || "").includes("Shopee") ? "bg-orange-100 text-orange-800" :
                                                                "bg-blue-100 text-blue-800"
                                                    )}>
                                                        {order.platform || "未知"}
                                                    </span>
                                                </td>
                                                {columns.map(col => (
                                                    <td key={col} className="px-4 py-4">
                                                        {getField(col)}
                                                    </td>
                                                ))}
                                            </tr>
                                        );
                                    })
                                )}
                            </tbody>
                        </table>
                    </div>
                </CardContent>
            </Card>
        </div>
    );
}

