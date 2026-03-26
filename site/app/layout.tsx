import "./globals.css";

import type { Metadata } from 'next';
import { Inter } from "next/font/google";
import zealtConfig from "@/zealt/config.json";
import { ThemeProvider } from "@/components/theme-provider";
import { ThemeToggle } from "@/components/theme-toggle";
import { AppQueryProvider } from "@/components/query-provider";

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
    <html lang="en" suppressHydrationWarning>
      <body className={`${inter.className} antialiased`}>
        <AppQueryProvider>
          <ThemeProvider defaultTheme="dark">
            <div className="fixed right-4 top-6 z-50 sm:top-8">
              <ThemeToggle />
            </div>
            {children}
          </ThemeProvider>
        </AppQueryProvider>
      </body>
    </html>
  );
}
