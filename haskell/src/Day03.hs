module Day03(run) where

import Data.Char (isDigit)

data Token = Number { start :: Int, _end ::  Int, _value :: Int } | Symbol { start :: Int, _char :: Char } deriving Show
isGear :: Token -> Bool
isGear (Symbol _ '*') = True
isGear _ = False

getValue :: Token -> Int
getValue Symbol {} = 0
getValue (Number _ _ n) = n
  
prod :: [Token] -> Int
prod (x:xs) = getValue x * prod xs
prod _ = 1
  
-- Tokenizing --
addNumber :: [(Int, Char)] -> [Token]
addNumber line = case span (isDigit . snd) line of
  ([], xs) -> tokenize xs
  (x, xs)  -> Number ((fst . head) x) ((fst . last) x) (read $ map snd x):tokenize xs


tokenize :: [(Int, Char)] -> [Token]
tokenize line = case line of
  (_, '.'):xs -> tokenize xs
  (i, x):xs   -> if isDigit x then addNumber line else Symbol i x:tokenize xs
  _           -> []

-- Neighbor Map Generation --
overlap :: Token -> Token -> Bool
overlap Symbol {} Symbol {} = False
overlap Number {} Number {} = False
overlap (Number a b c) (Symbol d e) = overlap (Symbol d e) (Number a b c)
overlap (Symbol d _) (Number a b _) = d >= a - 1 && d <= b + 1

getNeighbors :: [Token] -> Token -> [Token]
getNeighbors (x:xs) b = getNeighbors xs b ++ [x | overlap x b]
getNeighbors _ _ = []

mapNeighbors :: [Token] -> [Token] -> [(Token, [Token])]
mapNeighbors line around = filter (not . null . snd) . map (\x -> (x, getNeighbors around x)) $ line

generateNeighbors :: [[Token]] -> [(Token, [Token])]
generateNeighbors lst = case lst of
  a:b:c:xs  -> mapNeighbors b (a ++ b ++ c) ++ generateNeighbors (b:c:xs)
  a:b:_     -> mapNeighbors b (a ++ b)
  a:_       -> mapNeighbors a a
  _         -> []

-- Main -- 
run :: IO String -> IO ()
run input = do
  neighbors <- generateNeighbors . ([] :) . map (tokenize . zip [1..]) . lines <$> input
  print $ sum . map (getValue . fst) $ neighbors
  print $ sum . map prod . filter ((== 2) . length) . map snd . filter (isGear . fst) $ neighbors