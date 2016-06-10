## trajectories.rb

#index of car to follow
cari = 10

# which network output to process
networkname = ARGV[0]
if ARGV[0] == nil
  networkname = "huntcol"
end

f = File.open("./network/#{networkname}.output.xml", "r") # VTypeProbe output
lines = f.readlines
f.close

fo = File.open("./network/#{networkname}.poutput.txt", "w")

index = 0
time = -1
timei = -1
dist = 0
currx = 0; curry = 0;

while index < lines.length
  #puts index
  if lines[index] =~ /<timestep time="(.*)">/
    time = $1.to_f
    timei = time.to_i
  end
  
  if lines[index] =~ /<vehicle id="(.*)" lane="(.*)" pos="(.*)" x="(.*)" y="(.*)".*/
    if $1.to_i == cari
      # adds distance (approx) travelled this interval
      dist += ((currx - $4.to_i)**2 + (curry - $5.to_i)**2)**(0.5) 
      currx = $4.to_i;
      curry = $5.to_i;
      fo.write("<t=#{timei} -- dist=#{dist}>\n")
    end
  end
  index += 1
end
fo.close