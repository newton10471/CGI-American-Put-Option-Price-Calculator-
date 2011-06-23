#!/usr/local/bin/ruby

# Simple CGI (Common Gateway Interface) script to compute the price  
# of an American put option using the binomial options pricing model.
# This borrows heavily from the pseudocode algorithm described at 
# http://en.wikipedia.org/wiki/Binomial_options_pricing_model.
# 
# Matt Newton newton10471 at gmail.com
# last updated 06/23/2011


include Math
require 'cgi'

def americanPut(t, s, k, r, sigma, q, n) 
#        t... expiration time
#        s... stock price
#        k... strike price
#        r... risk-free interest rate
#        sigma ... volatility
#        n... height of the binomial tree

  deltaT = t / n
  up = exp(sigma * sqrt(deltaT))
  p0 = (up* exp(-r * deltaT) - exp(-q * deltaT)) * up / (up**2 - 1)
  p1 = exp(-r * deltaT ) - p0
  p = []

  (0..n).each do |i| 
    p[i] = k - s * up**(2 * i - n)
    if p[i] < 0 
      p[i] = 0
    end
  end

  (n-1).downto(0) do |j| 
    (0..j).each do |i|
      p[i] = p0 * p[i] + p1 * p[i+1]
      exercise = k - s * up**(2 * i - j)
      if p[i] < exercise 
        p[i] = exercise
      end
    end
  end

  return p[0]
end


# Create a cgi object, with HTML 4 generation methods.
cgi = CGI.new('html4')

# Ask the cgi object to send some text out to the browser.
cgi.out {
 cgi.html {
   cgi.body {
     cgi.h1 { "The option price is #{'%.2f' % americanPut(cgi['expiration'].to_f, cgi['stock_price'].to_f, cgi['strike_price'].to_f, cgi['interest_rate'].to_f, cgi['sigma'].to_f, 0, cgi['bintreesize'].to_i).round(2)}" }
   }
 }
}
