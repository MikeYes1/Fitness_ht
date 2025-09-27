'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export default function NavBar() {
  const pathname = usePathname();

  const navItems = [
    { href: '/', label: 'Home' },
    { href: '/dashboard', label: 'Dashboard' },
    { href: '/calendar', label: 'Calendar' },
    { href: '/chat', label: 'Chat' },
  ];

  return (
    <nav className="shadow-sm border-b sticky top-0 z-50" style={{backgroundColor: '#B7410E'}}>
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex items-center h-16">
          {/* Left Navigation Links */}
          <div className="flex items-center space-x-8">
            {navItems.slice(0, 2).map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`text-sm font-medium transition-colors duration-200 px-3 py-2 rounded-md uppercase tracking-wide ${
                    isActive
                      ? 'text-white'
                      : 'hover:bg-gray-100'
                  }`}
                  style={{
                    backgroundColor: isActive ? '#FFD700' : 'transparent',
                    color: isActive ? '#0F172A' : '#FFFFFF'
                  }}
                >
                  {item.label}
                </Link>
              );
            })}
          </div>

          {/* Center Brand */}
          <div className="flex-1 flex justify-center">
            <Link href="/" className="flex items-center space-x-2">
              <img src="/transparentlogo.png" alt="Fitness Planner" className="w-8 h-8" />
              <span className="text-xl font-bold uppercase tracking-wide" style={{color: '#FFFFFF'}}>Fitness Planner</span>
            </Link>
          </div>

          {/* Right Navigation Links */}
          <div className="flex items-center space-x-8">
            {navItems.slice(2).map((item) => {
              const isActive = pathname === item.href;
              return (
                <Link
                  key={item.href}
                  href={item.href}
                  className={`text-sm font-medium transition-colors duration-200 px-3 py-2 rounded-md uppercase tracking-wide ${
                    isActive
                      ? 'text-white'
                      : 'hover:bg-gray-100'
                  }`}
                  style={{
                    backgroundColor: isActive ? '#FFD700' : 'transparent',
                    color: isActive ? '#0F172A' : '#FFFFFF'
                  }}
                >
                  {item.label}
                </Link>
              );
            })}
          </div>
        </div>
      </div>
    </nav>
  );
}
