import "./globals.css";

import type { Metadata } from 'next';
import { Inter } from "next/font/google";
import zealtConfig from "@/zealt/config.json";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: zealtConfig.title,
  description: zealtConfig.description,
};


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en" className="dark">
      <body className={`${inter.className} antialiased`}>{children}</body>
    </html>
  );
}
