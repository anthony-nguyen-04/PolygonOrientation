%whiteImage = 255 * zeros(480, 640, 'uint8');
% why is (0,0) top left instead of bottom left
picture = imread("flower.jpg");
imshow(picture);

% draws polygon on top of image
h = drawpolygon('FaceAlpha', 0, 'Color', 'red');

points = h.Position;
range = (1:length(points))';

c = [range points];

% because y-axis is inverted, you have to sort y in descending order
sorted = sortrows(c,3, 'descend');

numPoints = length(c);

% gets index of top element
bottomIndex = int8(sorted(1,1));

% scrapes points for bottom point and its two adjacenet points
bottomPoint = [c(bottomIndex, 2) c(bottomIndex, 3)];

beforePoint = [c(mod((bottomIndex - 1) - 1, numPoints) + 1, 2) ...
    c(mod((bottomIndex - 1) - 1, numPoints) + 1, 3)];

afterPoint = [c(mod((bottomIndex + 1) - 1, numPoints) + 1, 2) ...
    c(mod((bottomIndex + 1) - 1, numPoints) + 1, 3)];

% gets vectors
beforeVector = [(beforePoint - bottomPoint) 0];
afterVector = [(afterPoint - bottomPoint) 0];

% gets cross product
zCross =(beforePoint(1) .* afterPoint(2)) - (beforePoint(2) .* afterPoint(1));

% determines direction
if zCross > 0
    direction = "clockwise"
    disp("clockwise");
elseif zCross < 0
    direction = "counter-clockwise";
    disp("counter-clockwise");
else
    direction = "collinear";
    disp("collinear");
end

% gets area selected by polygon
mask = createMask(h);

% based on orientation of polygon, turns ROI black or white
if direction == "clockwise"
    removed = imoverlay(picture, mask, "black"); 
elseif direction == "counter-clockwise"
   removed = imoverlay(picture, mask, "white");
else
    removed = picture;
end

% show image
imshow(removed);

disp(c);

% disp(sorted);
% disp(bottomIndex);
% disp(bottomPoint);
% disp(beforePoint);
% disp(afterPoint);
