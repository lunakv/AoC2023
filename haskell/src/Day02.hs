module Day02 (run) where
 
import Lib

data Count = Count Int Int Int deriving Show

instance Semigroup Count where
  (<>) (Count a b c) (Count x y z) = Count (max a x) (max b y) (max c z)
   
instance Monoid Count where
  mempty = Count 0 0 0
  
readCount :: String -> Count
readCount s = case words s of
  i:"red":_ -> Count (read i) 0 0
  i:"green":_ -> Count 0 (read i) 0
  i:"blue":_ -> Count 0 0 (read i)
  _ -> Count 0 0 0
  
score :: Num a => a -> Count -> a
score i (Count a b c) = if a <= 12 && b <= 13 && c <= 14 then i else 0

power :: Count -> Int
power (Count a b c) = a * b * c

maxPull :: String -> Count
maxPull = foldMap (foldMap readCount . split ',') . split ';'

matchingTotal :: [String] -> Integer
matchingTotal = sum . zipWith score [1..] . map maxPull

totalPower :: [String] -> Int
totalPower = sum . map (power . maxPull)

getPulls :: String -> String
getPulls line = split ':' line !! 1

run :: IO String -> IO ()
run s = do
  print . matchingTotal . map getPulls . lines =<< s
  print . totalPower . map getPulls . lines =<< s