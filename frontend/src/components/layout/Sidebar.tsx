"use client";

import React from "react";
import Link from "next/link";
import { usePathname } from "next/navigation";
import { LayoutDashboard, PackageSearch, ShoppingCart, Calculator, Settings } from "lucide-react";
import { cn } from "@/lib/utils";

const NAV_ITEMS = [
    { name: "總覽 Dashboard", href: "/", icon: LayoutDashboard },
    { name: "商品管理 Products", href: "/products", icon: PackageSearch },
    { name: "訂單管理 Orders", href: "/orders", icon: ShoppingCart },
    { name: "對帳報表 Reconciliations", href: "/reconciliations", icon: Calculator },
    { name: "設定 Settings", href: "/settings", icon: Settings },
];

export function Sidebar() {
    const pathname = usePathname();

    return (
        <div className="flex flex-col w-64 bg-card border-r border-border h-screen sticky top-0">
            <div className="flex items-center justify-center h-16 border-b border-border">
                <h1 className="text-xl font-bold text-primary flex items-center space-x-2">
                    <PackageSearch className="w-6 h-6" />
                    <span>Goods Manager</span>
                </h1>
            </div>
            <nav className="flex-1 overflow-y-auto py-4">
                <ul className="space-y-1.5 px-3">
                    {NAV_ITEMS.map((item) => {
                        const isActive = pathname === item.href;
                        const Icon = item.icon;
                        return (
                            <li key={item.name}>
                                <Link
                                    href={item.href}
                                    className={cn(
                                        "flex items-center px-4 py-2.5 rounded-lg text-sm font-medium transition-colors",
                                        isActive
                                            ? "bg-primary text-primary-foreground"
                                            : "text-secondary-foreground hover:bg-secondary hover:text-foreground"
                                    )}
                                >
                                    <Icon className={cn("w-5 h-5 mr-3", isActive ? "text-primary-foreground" : "text-slate-400")} />
                                    {item.name}
                                </Link>
                            </li>
                        );
                    })}
                </ul>
            </nav>
            <div className="p-4 border-t border-border">
                <div className="flex items-center space-x-3 text-sm">
                    <div className="w-8 h-8 rounded-full bg-primary/20 flex items-center justify-center text-primary font-bold">
                        U
                    </div>
                    <div>
                        <p className="font-medium">User Admin</p>
                        <p className="text-xs text-secondary-foreground">Online</p>
                    </div>
                </div>
            </div>
        </div>
    );
}
