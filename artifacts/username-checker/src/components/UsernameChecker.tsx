import React, { useState, useMemo } from 'react';
import { Input } from '@/components/ui/input';
import { Button } from '@/components/ui/button';
import { Card, CardContent } from '@/components/ui/card';
import { Search, CheckCircle2, XCircle, ExternalLink, ArrowRight } from 'lucide-react';
import { cn } from '@/lib/utils';

export function UsernameChecker() {
  const [input, setInput] = useState('');

  const validation = useMemo(() => {
    if (!input) return { state: 'empty' as const };
    
    const username = input.replace(/^@/, '');
    
    if (username.length < 5) return { state: 'invalid' as const, reason: 'Must be at least 5 characters', cleanUsername: username };
    if (username.length > 32) return { state: 'invalid' as const, reason: 'Cannot exceed 32 characters', cleanUsername: username };
    
    if (!/^[a-zA-Z0-9_]+$/.test(username)) {
      return { state: 'invalid' as const, reason: 'Only letters, numbers, and underscores allowed', cleanUsername: username };
    }
    
    if (/^[0-9]/.test(username)) {
      return { state: 'invalid' as const, reason: 'Cannot start with a number', cleanUsername: username };
    }
    
    return { state: 'valid' as const, reason: 'Valid username format', cleanUsername: username };
  }, [input]);

  const handleOpenTelegram = () => {
    if (validation.state === 'valid' && validation.cleanUsername) {
      window.open(`https://t.me/${validation.cleanUsername}`, '_blank', 'noopener,noreferrer');
    }
  };

  return (
    <div className="w-full max-w-md mx-auto space-y-8 animate-in fade-in slide-in-from-bottom-4 duration-500">
      <div className="text-center space-y-3">
        <div className="w-12 h-12 bg-primary/10 rounded-2xl flex items-center justify-center mx-auto mb-6 text-primary shadow-sm ring-1 ring-primary/20">
          <Search className="w-6 h-6" />
        </div>
        <h1 className="text-3xl font-bold tracking-tight text-foreground">
          Username Checker
        </h1>
        <p className="text-muted-foreground">
          Instantly validate and open any Telegram username.
        </p>
      </div>

      <div className="space-y-4">
        <div className="relative group">
          <div className="absolute inset-y-0 left-4 flex items-center pointer-events-none">
            <span className={cn(
              "text-lg transition-colors font-medium",
              input ? "text-foreground" : "text-muted-foreground/50"
            )}>@</span>
          </div>
          <Input
            type="text"
            placeholder="username"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="pl-9 h-14 text-lg bg-card border-2 transition-all duration-200 hover:border-primary/50 focus-visible:ring-4 focus-visible:ring-primary/20 focus-visible:border-primary rounded-xl shadow-sm"
            autoComplete="off"
            autoCorrect="off"
            autoCapitalize="off"
            spellCheck="false"
          />
          {validation.state === 'valid' && (
            <div className="absolute inset-y-0 right-4 flex items-center pointer-events-none text-emerald-500 animate-in zoom-in duration-300">
              <CheckCircle2 className="w-5 h-5" />
            </div>
          )}
          {validation.state === 'invalid' && (
            <div className="absolute inset-y-0 right-4 flex items-center pointer-events-none text-destructive animate-in zoom-in duration-300">
              <XCircle className="w-5 h-5" />
            </div>
          )}
        </div>

        <div className="min-h-[140px]">
          {validation.state === 'empty' && (
            <div className="h-full flex flex-col items-center justify-center text-center p-6 text-muted-foreground/60 border-2 border-dashed border-border rounded-xl bg-card/50">
              <p className="text-sm font-medium">Type a username to check</p>
            </div>
          )}

          {validation.state === 'invalid' && (
            <Card className="border-destructive/20 bg-destructive/5 shadow-none overflow-hidden animate-in fade-in slide-in-from-top-2 duration-300 rounded-xl">
              <CardContent className="p-4 flex items-start gap-3 text-destructive">
                <XCircle className="w-5 h-5 mt-0.5 shrink-0" />
                <div className="space-y-1">
                  <p className="font-medium">Invalid Format</p>
                  <p className="text-sm text-destructive/80">{validation.reason}</p>
                </div>
              </CardContent>
            </Card>
          )}

          {validation.state === 'valid' && validation.cleanUsername && (
            <Card className="border-primary/20 bg-primary/5 shadow-none overflow-hidden animate-in fade-in slide-in-from-top-2 duration-300 rounded-xl">
              <CardContent className="p-5 flex flex-col gap-5">
                <div className="flex items-start gap-3 text-primary">
                  <CheckCircle2 className="w-5 h-5 mt-0.5 shrink-0" />
                  <div className="space-y-1">
                    <p className="font-medium text-foreground">Looks good to go</p>
                    <p className="text-sm font-mono text-muted-foreground break-all">
                      t.me/{validation.cleanUsername}
                    </p>
                  </div>
                </div>
                
                <Button 
                  onClick={handleOpenTelegram}
                  className="w-full h-12 text-base font-semibold shadow-md shadow-primary/20 hover:shadow-lg hover:shadow-primary/30 transition-all rounded-lg group"
                >
                  Open on Telegram
                  <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-1 transition-transform" />
                </Button>
              </CardContent>
            </Card>
          )}
        </div>
      </div>
    </div>
  );
}
