import type { Metadata } from "next";
import { Mukta, Baloo_2 } from "next/font/google";
import "./globals.css";

const mukta = Mukta({
  variable: "--font-mukta",
  subsets: ["devanagari", "latin"],
  weight: ["400", "500", "600", "700"],
});

const baloo = Baloo_2({
  variable: "--font-baloo",
  subsets: ["devanagari", "latin"],
  weight: ["400", "500", "600", "700", "800"],
});

export const metadata: Metadata = {
  title: "Daily Paripath Generator (रोजचा परिपाठ)",
  description: "Generate beautiful Marathi Paripath boards daily.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="mr">
      <head>
          <link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.0.0/css/all.min.css" rel="stylesheet" />
      </head>
      <body
        className={`${mukta.variable} ${baloo.variable} antialiased`}
      >
        {children}
      </body>
    </html>
  );
}
